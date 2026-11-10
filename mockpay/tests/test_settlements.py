"""GET /v1/settlements: fees, refunds and the net payout."""

from datetime import date

import pytest
from fastapi.testclient import TestClient

from mockpay.money import fee_paise, format_inr
from mockpay.settlements import build_report
from tests.helpers import AUTH, captured_payment, create_order, get_json, pay


@pytest.mark.parametrize(
    ("amount", "fee"),
    [
        (10_000, 200),  # 2% of ₹100.00 is exactly ₹2.00
        (12_345, 247),  # 246.9 paise rounds up to 247
        (124, 2),  # 2.48 rounds down to 2
        (125, 3),  # 2.5: exactly half a paisa rounds up
        (175, 4),  # 3.5 rounds up to 4 (Python's round() would say 4 here, but 2 for 2.5)
        (100, 2),
    ],
)
def test_fee_is_two_percent_rounded_to_the_nearest_paisa(amount: int, fee: int) -> None:
    assert fee_paise(amount) == fee


def test_report_maths() -> None:
    captured = [
        {"id": "pay_a", "order_id": "order_a", "amount_paise": 10_000, "captured_at": "t1"},
        {"id": "pay_b", "order_id": "order_b", "amount_paise": 12_345, "captured_at": "t2"},
        {"id": "pay_c", "order_id": "order_c", "amount_paise": 125, "captured_at": "t3"},
    ]
    refunds = [
        {
            "id": "rfnd_a",
            "payment_id": "pay_a",
            "order_id": "order_a",
            "amount_paise": 5_000,
            "created_at": "t4",
        },
    ]

    report = build_report(date(2026, 11, 10), captured, refunds)

    assert [line["fee_paise"] for line in report["payments"]] == [200, 247, 3]
    assert report["captured_paise"] == 22_470
    assert report["refunded_paise"] == 5_000
    assert report["fees_paise"] == 450
    assert report["net_payout_paise"] == 22_470 - 5_000 - 450 == 17_020


def test_a_day_with_more_refunds_than_payments_has_a_negative_payout() -> None:
    refunds = [
        {
            "id": "rfnd_a",
            "payment_id": "pay_old",
            "order_id": "order_old",
            "amount_paise": 3_000,
            "created_at": "t",
        }
    ]
    report = build_report(date(2026, 11, 11), [], refunds)
    assert report["net_payout_paise"] == -3_000


def test_settlement_report_from_the_api(client: TestClient) -> None:
    first = captured_payment(client, 10_000)
    captured_payment(client, 12_345)
    captured_payment(client, 125)
    declined_order = create_order(client, 50_000)
    pay(client, declined_order["id"], "decline")  # failed payments are not settled
    client.post("/v1/refunds", json={"payment_id": first, "amount_paise": 5_000}, headers=AUTH)
    day = get_json(client, f"/v1/payments/{first}")["captured_at"][:10]

    report = get_json(client, f"/v1/settlements?date={day}")

    assert report["date"] == day
    assert len(report["payments"]) == 3
    assert len(report["refunds"]) == 1
    assert report["captured_paise"] == 22_470
    assert report["fees_paise"] == 450
    assert report["refunded_paise"] == 5_000
    assert report["net_payout_paise"] == 17_020


def test_a_day_without_payments_is_empty(client: TestClient) -> None:
    captured_payment(client)

    report = get_json(client, "/v1/settlements?date=2000-01-01")

    assert report["payments"] == [] and report["refunds"] == []
    assert report["net_payout_paise"] == 0


def test_bad_date_is_400(client: TestClient) -> None:
    response = client.get("/v1/settlements?date=10-11-2026", headers=AUTH)
    assert response.status_code == 400


def test_rupee_formatting_uses_indian_digit_groups() -> None:
    assert format_inr(125_000) == "₹1,250.00"
    assert format_inr(12_345_678_900) == "₹12,34,56,789.00"
    assert format_inr(5) == "₹0.05"
    assert format_inr(-3_000) == "-₹30.00"
