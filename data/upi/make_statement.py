#!/usr/bin/env python3
"""Make a realistic but FAKE Indian bank statement as a CSV file.

This is the data for PaisaLens (P1). Each student makes their own file from
their student id, so no two students have the same data.

Run it from the folder that holds this file:

    uv run make_statement.py --student FSPY-0042 --months 6 --out statement.csv

(`python make_statement.py ...` works too; the script needs Python 3.10 or newer).
The same student id always gives exactly the same file, on any computer.

The CSV has six columns: date, narration, upi_ref, debit, credit, balance.
Amounts are in rupees with two decimals, for example 249.00. Your PaisaLens
code turns them into paise (whole numbers): 249.00 rupees is 24900 paise.

The data is messy on purpose, like a real bank export. README.md in this
folder explains what is messy and why.

The script uses only the Python standard library, so there is nothing to
install. Never use your real bank statement for the course.
"""

from __future__ import annotations

import argparse
import calendar
import csv
import hashlib
import random
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

HEADER = ["date", "narration", "upi_ref", "debit", "credit", "balance"]
DEFAULT_END_MONTH = "2026-10"  # the last month in the statement
DATE_FORMAT = "%d/%m/%Y"  # day/month/year, as most Indian banks export it
LOW_BALANCE_PAISE = 500_00  # always keep ₹500 in the account for optional spending
BROKEN_KINDS = ("bad_date", "empty_amount", "text_amount", "duplicate_ref")


# ---------------------------------------------------------------------------
# Random numbers that stay the same on every Python version
# ---------------------------------------------------------------------------

class Dice:
    """A small wrapper around random.Random.

    Python only promises that random() gives the same numbers for the same
    seed on every Python version. Helpers such as randint() and choice() have
    changed between versions in the past. So every helper here is built on
    random() alone, and a student's file is the same on Python 3.12 or 3.13.
    """

    def __init__(self, seed_text: str) -> None:
        # hash() changes every time Python starts, so we use SHA-256 instead.
        digest = hashlib.sha256(seed_text.encode("utf-8")).digest()
        self._rng = random.Random(int.from_bytes(digest[:8], "big"))

    def number(self, low: int, high: int) -> int:
        """A whole number from low to high, both included."""
        return low + int(self._rng.random() * (high - low + 1))

    def pick(self, items):
        """One item from a list, a tuple or a string."""
        return items[int(self._rng.random() * len(items))]

    def chance(self, probability: float) -> bool:
        """True with the given probability, for example 0.25 for one in four."""
        return self._rng.random() < probability

    def paise(self, low_rupees: int, high_rupees: int, whole_chance: float = 0.4) -> int:
        """An amount in paise between two rupee values.

        Four amounts in ten are whole rupees (like 450.00), and the rest have
        paise (like 312.45), as real bills do.
        """
        rupees = self.number(low_rupees, high_rupees - 1)
        paise = 0 if self.chance(whole_chance) else self.number(1, 99)
        return rupees * 100 + paise

    def shuffle(self, items: list) -> None:
        """Shuffle a list in place (the Fisher-Yates method)."""
        for i in range(len(items) - 1, 0, -1):
            j = self.number(0, i)
            items[i], items[j] = items[j], items[i]


# ---------------------------------------------------------------------------
# Who the money goes to
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Merchant:
    names: tuple[str, ...]  # the same merchant, written in different ways
    upi_ids: tuple[str, ...]  # UPI ids (VPAs) the merchant collects money on
    low: int  # smallest usual bill, in rupees
    high: int  # largest usual bill, in rupees


# Real company names are used because they make the data feel real.
# The legal names (for example BUNDL TECHNOLOGIES for Swiggy) are real too:
# banks often print the legal name instead of the brand name.
MERCHANTS: dict[str, Merchant] = {
    "swiggy": Merchant(("SWIGGY", "Swiggy Limited", "BUNDL TECHNOLOGIES", "swiggy food"),
                       ("swiggy.payu@hdfcbank", "swiggyupi@axisbank", "swiggy@icici"), 120, 780),
    "zomato": Merchant(("ZOMATO", "ZOMATO LTD", "Zomato Limited", "zomato order"),
                       ("zomato.payu@axisbank", "zomatoltd@ybl", "zomato@icici"), 140, 820),
    "blinkit": Merchant(("BLINKIT", "Blink Commerce Pvt Ltd", "blinkit.com"),
                        ("blinkit.payu@hdfcbank", "blinkit@icici"), 99, 1200),
    "zepto": Merchant(("ZEPTO", "KiranaKart Technologies", "Zepto Marketplace"),
                      ("zepto@ybl", "zeptonow@axisbank"), 89, 1100),
    "bigbasket": Merchant(("BIGBASKET", "Innovative Retail Concepts", "bigbasket.com"),
                          ("bigbasket@hdfcbank", "bbdaily@icici"), 450, 2600),
    "dmart": Merchant(("DMART", "AVENUE SUPERMARTS LTD", "D MART KOTHRUD"),
                      ("dmart.kothrud@icici", "avenuesupermarts@hdfcbank"), 300, 2400),
    "kirana": Merchant(("SHREE GANESH KIRANA STORES", "Ganesh Kirana", "GANESH PROVISION"),
                       ("q781245536@ybl", "ganeshkirana@okaxis"), 40, 650),
    "uber": Merchant(("UBER INDIA", "Uber India Systems Pvt", "UBER"),
                     ("uber.payu@icici", "uberindia@axisbank"), 89, 640),
    "ola": Merchant(("OLA", "ANI TECHNOLOGIES PVT LTD", "Ola Cabs"),
                    ("olacabs@ybl", "olamoney@hdfcbank"), 79, 590),
    "rapido": Merchant(("RAPIDO", "Roppen Transportation", "rapido bike taxi"),
                       ("rapido@ybl", "rapidobike@axisbank"), 35, 190),
    "metro": Merchant(("PUNE METRO", "MAHA METRO RAIL", "Maharashtra Metro Rail Corp"),
                      ("punemetro@sbi", "mahametro@icici"), 20, 70),
    "irctc": Merchant(("IRCTC", "IRCTC UTS", "Indian Railway Catering"),
                      ("irctc@hdfcbank", "irctcuts@sbi"), 150, 2400),
    "petrol": Merchant(("INDIAN OIL", "IOCL KOTHRUD", "Indian Oil Corp Ltd"),
                       ("iocl.kothrud@sbi", "indianoil@icici"), 200, 900),
    "amazon": Merchant(("AMAZON", "Amazon Pay India", "AMAZON SELLER SERVICES", "amazon.in"),
                       ("amazon@apl", "amazonpay@axisbank"), 199, 4999),
    "flipkart": Merchant(("FLIPKART", "Flipkart Internet Pvt Ltd", "FKRT"),
                         ("flipkart@axisbank", "fkrt@ybl"), 249, 5499),
    "myntra": Merchant(("MYNTRA", "Myntra Designs"),
                       ("myntra@icici", "myntrapayments@ybl"), 399, 2999),
    "meesho": Merchant(("MEESHO", "Fashnear Technologies"),
                       ("meesho@ybl", "meesho.payu@hdfcbank"), 149, 899),
    "chaipoint": Merchant(("CHAI POINT", "Mountain Trail Foods"),
                          ("chaipoint@icici", "chaipoint.mtf@ybl"), 40, 260),
    "mess": Merchant(("ANNAPURNA MESS", "Annapurna Veg Mess"),
                     ("q665120934@ybl", "annapurnamess@oksbi"), 60, 220),
    "cafe": Merchant(("HOTEL SAGAR VEG", "Sagar Veg Restaurant"),
                     ("sagarveg@okhdfcbank", "q550931882@ybl"), 150, 900),
    "apollo": Merchant(("APOLLO PHARMACY", "Apollo Pharmacies Ltd"),
                       ("apollopharmacy@icici", "apollo247@axisbank"), 60, 950),
    "medplus": Merchant(("MEDPLUS", "Optival Health Solutions"),
                        ("medplus@ybl", "medplusmart@hdfcbank"), 50, 800),
    "bookmyshow": Merchant(("BOOKMYSHOW", "Bigtree Entertainment", "bookmyshow.com"),
                           ("bookmyshow@icici", "bms@axisbank"), 180, 900),
    "pvr": Merchant(("PVR INOX", "PVR INOX LTD"),
                    ("pvrinox@icici",), 220, 1100),
    "msedcl": Merchant(("MSEDCL", "MAHAVITARAN", "Maharashtra State Electricity"),
                       ("msedcl@sbi", "mahavitaran@icici"), 380, 1700),
}

# Monthly subscriptions. They come back every month on nearly the same day.
# Their UPI ids always contain the merchant's name, so they can be found.
SUBSCRIPTIONS: dict[str, Merchant] = {
    "netflix": Merchant(("NETFLIX", "NETFLIX.COM", "Netflix Entertainment Services India LLP"),
                        ("netflix.autopay@icici", "netflixupi.payu@hdfcbank"), 0, 0),
    "spotify": Merchant(("SPOTIFY", "Spotify India LLP", "SPOTIFY PREMIUM"),
                        ("spotify.autopay@hdfcbank", "spotify@axisbank"), 0, 0),
    "cultfit": Merchant(("CULT.FIT", "CUREFIT HEALTHCARE PVT LTD", "cultfit"),
                        ("cultfit@icici", "curefit.payu@hdfcbank"), 0, 0),
    "ironzone": Merchant(("IRON ZONE GYM", "Iron Zone Fitness", "IRONZONE GYM BANER"),
                         ("ironzonegym@okaxis", "ironzone.fitness@ybl"), 0, 0),
    "airtel": Merchant(("AIRTEL", "Bharti Airtel Ltd", "AIRTEL POSTPAID"),
                       ("airtelpostpaid@airtel", "airtel.payu@icici"), 0, 0),
}

# Fictional people, for rent and for money sent between friends.
LANDLORDS = ("SURESH PATIL", "MEENA JOSHI", "RAJESH KULKARNI", "ANITA DESHPANDE")
FRIENDS = ("PRIYA SHARMA", "ROHAN DESAI", "AMIT KUMAR", "SNEHA IYER", "KARAN MEHTA",
           "FATIMA SHAIKH", "ARJUN NAIR", "DIVYA REDDY", "VIKRAM SINGH", "NEHA GUPTA")
FRIEND_HANDLES = ("okicici", "oksbi", "okaxis", "okhdfcbank", "ybl", "axl")
EMPLOYERS = ("NIMBUS SOFTWARE PVT LTD", "DECCAN DATA SYSTEMS PVT LTD",
             "SAHYADRI TECH SOLUTIONS LLP", "KAVERI INFOTECH PVT LTD")
ATM_PLACES = ("KOTHRUD PUNE", "SHIVAJINAGAR PUNE", "HINJEWADI PUNE", "BANER PUNE",
              "VIMAN NAGAR PUNE", "FC ROAD PUNE")

# The part after "@" in a UPI id names the bank or app that handles it.
# Each handle has a bank code, a sample IFSC (branch code) and a bank name.
HANDLES: dict[str, tuple[str, str, str]] = {
    "ybl": ("YESB", "YESB0YBLUPI", "YES BANK"),
    "axl": ("UTIB", "UTIB0000553", "AXIS BANK"),
    "okaxis": ("UTIB", "UTIB0000000", "AXIS BANK"),
    "oksbi": ("SBIN", "SBIN0000001", "STATE BANK OF INDIA"),
    "okhdfcbank": ("HDFC", "HDFC0000001", "HDFC BANK"),
    "okicici": ("ICIC", "ICIC0000001", "ICICI BANK"),
    "icici": ("ICIC", "ICIC0DC0099", "ICICI BANK"),
    "hdfcbank": ("HDFC", "HDFC0000499", "HDFC BANK"),
    "axisbank": ("UTIB", "UTIB0000100", "AXIS BANK"),
    "apl": ("UTIB", "UTIB0000114", "AXIS BANK"),
    "sbi": ("SBIN", "SBIN0016209", "STATE BANK OF INDIA"),
    "airtel": ("AIRP", "AIRP0000001", "AIRTEL PAYMENTS BANK"),
}

# Banks write UPI narrations in different layouts. We mix five common ones in
# one file, so your cleaning code has to handle all of them.
STYLES = ("slash", "dash", "ref_first", "p2m", "short")
MERCHANT_NOTES = ("Payment from Ph", "UPI", "Pay to merchant", "Paid via PhonePe", "Sent using Paytm")
MANDATE_NOTES = ("UPI Mandate", "AutoPay", "Mandate Execute")
FRIEND_NOTES = ("dinner", "dinner, cab", "trip share", "movie", "thanks", "chai and snacks", "groceries")


@dataclass
class Txn:
    """One line of the statement before the balance is worked out."""

    when: datetime  # date and time; the time is used only for sorting
    narration: str
    upi_ref: str  # empty for payments that are not UPI (ATM, NEFT, bank charges)
    debit: int  # paise taken out (0 if none)
    credit: int  # paise put in (0 if none)
    kind: str  # what sort of payment this is; used inside this script only
    optional: bool = False  # True for spending a person would skip when money is low
    merchant: str = ""  # key in MERCHANTS, for merchant payments
    refund_of: "Txn | None" = None  # for a refund: the purchase it gives money back for


# ---------------------------------------------------------------------------
# Building narrations, reference numbers and amounts
# ---------------------------------------------------------------------------

class RefMaker:
    """Makes 12-digit UPI reference numbers (RRNs), each one unique.

    A real UPI reference starts with the last digit of the year, then the day
    of the year (001-366), then the hour (00-23), then a 6-digit counter.
    """

    def __init__(self, dice: Dice) -> None:
        self.dice = dice
        self.used: set[str] = set()

    def new(self, when: datetime) -> str:
        while True:
            day_of_year = when.timetuple().tm_yday
            ref = f"{when.year % 10}{day_of_year:03d}{when.hour:02d}{self.dice.number(0, 999_999):06d}"
            if ref not in self.used:
                self.used.add(ref)
                return ref


def upi_narration(dice: Dice, style: str, direction: str, ref: str, name: str,
                  upi_id: str, note: str, person: bool = False) -> str:
    """Write a UPI narration in one of the five bank layouts."""
    bank_code, ifsc, bank_name = HANDLES[upi_id.split("@")[1]]
    if style == "slash":  # UPI/DR/412345678901/SWIGGY/YESB/swiggy@ybl/Payment from Ph
        return f"UPI/{direction}/{ref}/{name.upper()[:20]}/{bank_code}/{upi_id}/{note[:15]}"
    if style == "dash":  # UPI-ZOMATO LTD-zomato.payu@axisbank-UTIB0000100-412345678901-UPI
        return f"UPI-{name.upper()}-{upi_id}-{ifsc}-{ref}-{note.upper()}"
    if style == "ref_first":  # UPI/412345678901/Payment from Ph/swiggy@icici/Icici Bank/ICIa1b2...
        token = "".join(dice.pick("0123456789abcdef") for _ in range(12))
        return f"UPI/{ref}/{note}/{upi_id}/{bank_name.title()}/ICI{token}"
    if style == "p2m":  # UPI/P2M/412345678901/Swiggy Limited/Paid via PhonePe/YES BANK
        kind = "P2A" if person else "P2M"  # P2A = to a person, P2M = to a merchant
        return f"UPI/{kind}/{ref}/{name}/{note}/{bank_name}"
    return f"UPI/{name.upper()}/{ref}/{note}"  # "short": UPI/NETFLIX/412345678901/AutoPay


def friend_upi_id(dice: Dice, person: str) -> str:
    first, last = person.lower().split()
    return f"{first}.{last}{dice.number(1, 99)}@{dice.pick(FRIEND_HANDLES)}"


def money(paise: int) -> str:
    """Write paise as rupees with two decimals: 24900 -> '249.00'."""
    sign = "-" if paise < 0 else ""
    return f"{sign}{abs(paise) // 100}.{abs(paise) % 100:02d}"


# ---------------------------------------------------------------------------
# Dates
# ---------------------------------------------------------------------------

def month_list(end_month: str, months: int) -> list[tuple[int, int]]:
    """The (year, month) pairs covered, oldest first, ending with end_month."""
    year, month = (int(part) for part in end_month.split("-"))
    result = []
    for _ in range(months):
        result.append((year, month))
        month -= 1
        if month == 0:
            year, month = year - 1, 12
    return list(reversed(result))


def last_working_day(year: int, month: int) -> date:
    """Salaries arrive on the last weekday of the month (Monday to Friday)."""
    day = date(year, month, calendar.monthrange(year, month)[1])
    while day.weekday() >= 5:  # 5 is Saturday, 6 is Sunday
        day -= timedelta(days=1)
    return day


def at(dice: Dice, day: date, first_hour: int = 7, last_hour: int = 23) -> datetime:
    """A random time of day on the given date."""
    return datetime(day.year, day.month, day.day, dice.number(first_hour, last_hour), dice.number(0, 59))


# ---------------------------------------------------------------------------
# Making the transactions
# ---------------------------------------------------------------------------

def make_transactions(dice: Dice, months: list[tuple[int, int]]) -> list[Txn]:
    refs = RefMaker(dice)
    home_style = dice.pick(STYLES)  # this student's bank uses one layout most often

    def style() -> str:
        """Half the rows use the student's home layout; the rest use any of the five."""
        return home_style if dice.chance(0.5) else dice.pick(STYLES)

    # Things that stay the same for one student across all months.
    salary = dice.number(320, 680) * 100 * 100  # ₹32,000 to ₹68,000 a month
    rent = round(salary * dice.number(18, 28) / 100 / 100_00) * 100_00  # nearest ₹100
    landlord = dice.pick(LANDLORDS)
    landlord_id = friend_upi_id(dice, landlord)
    employer = dice.pick(EMPLOYERS)
    employer_ifsc = dice.pick(("HDFC0000240", "ICIC0000104", "UTIB0000062", "SBIN0001882"))
    card_last4 = f"{dice.number(1000, 9999)}"
    gym = dice.pick(("cultfit", "ironzone"))
    plans = {  # monthly price in paise and the usual day of the month (at most 26)
        "netflix": (dice.pick((149_00, 199_00, 499_00)), dice.number(3, 25)),
        "spotify": (dice.pick((119_00, 139_00)), dice.number(5, 26)),
        gym: (dice.pick((1299_00, 1499_00, 1999_00)), dice.number(1, 6)),
        "airtel": (0, dice.number(17, 22)),  # the Airtel bill changes a little every month
    }
    airtel_base = dice.pick((449_00, 549_00, 649_00))
    card_fee_month = dice.number(1, 12)
    lifestyle = salary / 45_000_00  # people who earn more spend more

    txns: list[Txn] = []

    def spend(kind: str, key: str, day: date) -> Txn:
        """A UPI payment to a merchant. The bill size depends on the merchant and the salary."""
        merchant = MERCHANTS[key]
        when = at(dice, day)
        ref = refs.new(when)
        factor = min(1.6, max(0.7, lifestyle))
        amount = dice.paise(max(10, int(merchant.low * factor)), max(11, int(merchant.high * factor)))
        note = dice.pick(MERCHANT_NOTES)
        text = upi_narration(dice, style(), "DR", ref, dice.pick(merchant.names), dice.pick(merchant.upi_ids), note)
        txn = Txn(when, text, ref, amount, 0, kind, optional=True, merchant=key)
        txns.append(txn)
        return txn

    for year, month in months:
        days = calendar.monthrange(year, month)[1]

        def any_day() -> date:
            return date(year, month, dice.number(1, days))

        # Salary by NEFT. NEFT is not UPI, so there is no upi_ref.
        pay_day = last_working_day(year, month)
        when = datetime(pay_day.year, pay_day.month, pay_day.day, dice.number(9, 13), dice.number(0, 59))
        utr = f"{employer_ifsc[:4]}N{year % 100:02d}{when.timetuple().tm_yday:03d}{dice.number(0, 999_999):06d}"
        month_name = calendar.month_abbr[month].upper()
        txns.append(Txn(when, f"NEFT CR-{employer_ifsc}-{employer}-SALARY {month_name} {year}-{utr}",
                        "", 0, salary, "salary"))

        # Rent to the landlord in the first five days of the month.
        when = at(dice, date(year, month, dice.number(1, 5)), 8, 21)
        ref = refs.new(when)
        note = f"rent {calendar.month_abbr[month].lower()}"
        txns.append(Txn(when, upi_narration(dice, style(), "DR", ref, landlord, landlord_id, note, person=True),
                        ref, rent, 0, "rent"))

        # Subscriptions: the same day each month, give or take a day or two.
        for key, (price, usual_day) in plans.items():
            drift = dice.pick((0, 0, 0, 1, 1, 2, -1))
            day = date(year, month, min(days, max(1, usual_day + drift)))
            when = at(dice, day, 0, 9)  # AutoPay usually runs early in the morning
            ref = refs.new(when)
            amount = price
            if key == "airtel":  # plan price + 18% GST, and a small extra in half the months
                amount = round(airtel_base * 118 / 100) + dice.pick((0, 0, 0, 1180, 2360, 5900))
            merchant = SUBSCRIPTIONS[key]
            text = upi_narration(dice, style(), "DR", ref, dice.pick(merchant.names),
                                 dice.pick(merchant.upi_ids), dice.pick(MANDATE_NOTES))
            txns.append(Txn(when, text, ref, amount, 0, "subscription"))

        # Electricity bill: paid every month, but not on a fixed day.
        spend("bill", "msedcl", date(year, month, dice.number(8, 15))).optional = False

        # Everyday spending.
        for _ in range(dice.number(6, 9)):
            spend("food", dice.pick(("swiggy", "swiggy", "zomato", "zomato")), any_day())
        for _ in range(dice.number(3, 5)):
            spend("grocery", dice.pick(("blinkit", "zepto", "bigbasket", "dmart", "kirana", "kirana")), any_day())
        for _ in range(dice.number(2, 4)):
            spend("transport", dice.pick(("uber", "ola", "rapido", "rapido", "metro", "petrol")), any_day())
        for _ in range(dice.number(1, 2)):
            spend("shopping", dice.pick(("amazon", "amazon", "flipkart", "myntra", "meesho")), any_day())
        for _ in range(dice.number(1, 3)):
            spend("eating_out", dice.pick(("chaipoint", "mess", "cafe")), any_day())
        if dice.chance(0.6):
            spend("health", dice.pick(("apollo", "medplus")), any_day())
        if dice.chance(0.5):
            spend("entertainment", dice.pick(("bookmyshow", "pvr")), any_day())
        if dice.chance(0.3):
            spend("travel", "irctc", any_day())

        # Money sent to friends, and money friends send back.
        for _ in range(dice.number(1, 2)):
            person = dice.pick(FRIENDS)
            when = at(dice, any_day())
            ref = refs.new(when)
            amount = dice.pick((150, 200, 250, 300, 400, 500, 750, 1000, 1200)) * 100
            text = upi_narration(dice, style(), "DR", ref, person, friend_upi_id(dice, person),
                                 dice.pick(FRIEND_NOTES), person=True)
            txns.append(Txn(when, text, ref, amount, 0, "friend_out", optional=True))
        for _ in range(dice.number(0, 2)):
            person = dice.pick(FRIENDS)
            when = at(dice, any_day())
            ref = refs.new(when)
            amount = dice.pick((120, 180, 250, 300, 350, 500, 600)) * 100
            text = upi_narration(dice, style(), "CR", ref, person, friend_upi_id(dice, person),
                                 dice.pick(FRIEND_NOTES), person=True)
            txns.append(Txn(when, text, ref, 0, amount, "friend_in"))

        # Cash from an ATM. ATM withdrawals are not UPI, so there is no upi_ref.
        for _ in range(dice.number(1, 2)):
            when = at(dice, any_day(), 8, 22)
            place = dice.pick(ATM_PLACES)
            atm_id = dice.number(1000, 9999)
            text = dice.pick((f"ATW-512967XXXXXX{card_last4}-S1AN{atm_id}-{place}",
                              f"NWD-512967XXXXXX{card_last4}-SPCN{atm_id}-{place}",
                              f"ATM CASH WDL {card_last4} {place}"))
            amount = dice.pick((500, 1000, 1500, 2000, 2000, 3000, 5000)) * 100
            txns.append(Txn(when, text, "", amount, 0, "atm", optional=True))

        # Bank interest and charges at the end of each quarter (March, June, September, December).
        if month in (3, 6, 9, 12):
            quarter_start = date(year, month - 2, 1)
            quarter_end = date(year, month, days)
            when = datetime(year, month, days, 23, 30)
            txns.append(Txn(when, f"INT.PD:{quarter_start:%d-%m-%Y} TO {quarter_end:%d-%m-%Y}",
                            "", 0, dice.paise(40, 320, whole_chance=0), "interest"))
            txns.append(Txn(when - timedelta(minutes=5), f"SMS CHGS QTR {month_name}-{year}+GST",
                            "", 17_70, 0, "charges"))
        if month == card_fee_month:
            when = at(dice, date(year, month, dice.number(2, 10)), 1, 4)
            txns.append(Txn(when, f"DC ANNUAL FEE {card_last4} + GST", "", 236_00, 0, "charges"))

    add_refunds(dice, refs, txns, style, months)
    return txns


def add_refunds(dice: Dice, refs: RefMaker, txns: list[Txn], style, months: list[tuple[int, int]]) -> None:
    """Add about one refund a month, each for an earlier purchase."""
    last_day = date(*months[-1], calendar.monthrange(*months[-1])[1])
    purchases = sorted((t for t in txns if t.kind in ("shopping", "food")), key=lambda t: t.when)
    for year, month in months:
        in_month = [t for t in purchases if (t.when.year, t.when.month) == (year, month)]
        if not in_month or not dice.chance(0.85):
            continue
        original = dice.pick(in_month)
        if original.kind == "shopping":
            # A returned item: the shop sends the money back a few days later.
            refund_day = original.when.date() + timedelta(days=dice.number(3, 9))
            if refund_day > last_day:
                continue
            merchant = MERCHANTS[original.merchant]
            when = at(dice, refund_day)
            ref = refs.new(when)
            text = upi_narration(dice, style(), "CR", ref, dice.pick(merchant.names),
                                 dice.pick(merchant.upi_ids), "Refund")
            txns.append(Txn(when, text, ref, 0, original.debit, "refund", refund_of=original))
        else:
            # A failed food order: the money comes back the same day, as a reversal.
            # The reversal names the original payment's reference in its narration.
            when = original.when + timedelta(minutes=dice.number(20, 90))
            if when.date() > last_day:
                continue
            ref = refs.new(when)
            name = original.merchant.upper()  # SWIGGY or ZOMATO
            txns.append(Txn(when, f"REV-UPI-{original.upi_ref}-{name}-FAILED TXN", ref, 0, original.debit,
                            "refund", refund_of=original))


# ---------------------------------------------------------------------------
# Balances, broken rows and the final rows
# ---------------------------------------------------------------------------

def with_balances(dice: Dice, txns: list[Txn]) -> list[tuple[Txn, int]]:
    """Sort the transactions by time and work out the running balance.

    Optional spending is skipped when it would leave less than ₹500 plus the
    rent, bills and subscriptions still due before the next salary. That is
    what a careful person does, and it keeps the balance above zero.
    """
    order = sorted(range(len(txns)), key=lambda i: (txns[i].when, i))
    # Walk backwards to find, for each transaction, the fixed costs that are
    # still to be paid after it and before the next salary arrives.
    still_due = [0] * len(order)
    due = 0
    for k in range(len(order) - 1, -1, -1):
        txn = txns[order[k]]
        still_due[k] = due
        if txn.kind == "salary":
            due = 0
        elif not txn.optional:
            due += txn.debit
    months_covered = len({(t.when.year, t.when.month) for t in txns})
    fixed_per_month = sum(t.debit for t in txns if not t.optional) // max(1, months_covered)
    # The opening balance covers one month of fixed costs, plus savings of ₹8,000 to ₹30,000.
    balance = fixed_per_month + dice.number(8_000, 30_000) * 100 + dice.number(0, 99)
    rows = []
    skipped: set[int] = set()  # id() of every transaction left out
    for k, i in enumerate(order):
        txn = txns[i]
        if txn.optional and txn.debit and balance - txn.debit < LOW_BALANCE_PAISE + still_due[k]:
            skipped.add(id(txn))
            continue
        if txn.refund_of is not None and id(txn.refund_of) in skipped:
            continue  # no refund for a purchase that never happened
        balance = balance - txn.debit + txn.credit
        rows.append((txn, balance))
    return rows


def break_some_rows(dice: Dice, rows: list[list[str]], kinds: list[str]) -> dict[str, int]:
    """Damage four rows on purpose, one of each kind, like a real messy export.

    - bad_date: a date that cannot exist, such as 31/09/2026
    - empty_amount: both debit and credit are empty, but the balance still moves
    - text_amount: the debit is written as text, such as Rs.855/-
    - duplicate_ref: the row appears twice, so its upi_ref is there twice

    Returns where each broken row ended up (a 0-based index into rows).
    """
    # Only everyday UPI spending is damaged, never salary, rent or subscriptions.
    candidates = [i for i in range(2, len(rows) - 2)
                  if kinds[i] in ("food", "grocery", "transport", "shopping", "eating_out") and rows[i][3]]
    dice.shuffle(candidates)
    # The text amount is chosen first, from whole-rupee amounts if possible,
    # because "Rs.450/-" is how people write a whole-rupee amount in India.
    whole_rupees = [i for i in candidates if rows[i][3].endswith(".00")]
    chosen: list[int] = [whole_rupees[0] if whole_rupees else candidates[0]]
    for gap in (3, 2):  # keep broken rows apart; a very short statement may need a smaller gap
        for i in candidates:
            if len(chosen) < 4 and i not in chosen and all(abs(i - j) >= gap for j in chosen):
                chosen.append(i)
    if len(chosen) < 4:
        raise ValueError("the statement is too short to hold the broken rows; use more months")
    text_row, bad_date_row, empty_row, duplicate_row = chosen

    day, month, year = (int(part) for part in rows[bad_date_row][0].split("/"))
    days_in_month = calendar.monthrange(year, month)[1]
    impossible_day = 30 if month == 2 else (31 if days_in_month == 30 else 32)
    rows[bad_date_row][0] = f"{impossible_day:02d}/{month:02d}/{year}"
    rows[empty_row][3] = ""
    amount = rows[text_row][3]
    rows[text_row][3] = f"Rs.{amount[:-3] if amount.endswith('.00') else amount}/-"  # like Rs.855/-
    rows.insert(duplicate_row + 1, list(rows[duplicate_row]))

    def moved(i: int) -> int:
        """Rows after the inserted copy have moved down by one place."""
        return i + 1 if i > duplicate_row else i

    return {"bad_date": moved(bad_date_row), "empty_amount": moved(empty_row),
            "text_amount": moved(text_row), "duplicate_ref": duplicate_row + 1}


def generate(student: str, months: int = 6, end_month: str = DEFAULT_END_MONTH) -> tuple[list[list[str]], dict[str, int]]:
    """Make the statement rows (without the header) for one student.

    Returns the rows and a map of which rows were broken on purpose.
    """
    dice = Dice(f"paisalens|{student.strip().upper()}")
    txns = make_transactions(dice, month_list(end_month, months))
    rows_with_balance = with_balances(dice, txns)
    rows = [[txn.when.strftime(DATE_FORMAT), txn.narration, txn.upi_ref,
             money(txn.debit) if txn.debit else "", money(txn.credit) if txn.credit else "", money(balance)]
            for txn, balance in rows_with_balance]
    kinds = [txn.kind for txn, _ in rows_with_balance]
    broken = break_some_rows(dice, rows, kinds)
    return rows, broken


def write_csv(path: Path, rows: list[list[str]]) -> None:
    # newline="" and lineterminator="\n" give the same bytes on Windows, macOS and Linux.
    # The csv module puts quotes around a value that holds a comma, such as "dinner, cab".
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(HEADER)
        writer.writerows(rows)


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Make a fake Indian bank statement CSV for PaisaLens (P1). "
                    "Never use your real bank statement.")
    parser.add_argument("--student", required=True, help="your student id, for example FSPY-0042")
    parser.add_argument("--months", type=int, default=6, help="how many months to cover (1 to 24, default 6)")
    parser.add_argument("--out", default="statement.csv", help="where to write the CSV (default statement.csv)")
    parser.add_argument("--end-month", default=DEFAULT_END_MONTH,
                        help=f"the last month in the statement, as YYYY-MM (default {DEFAULT_END_MONTH})")
    args = parser.parse_args(argv)
    if not args.student.strip():
        parser.error("--student must not be empty")
    if not 1 <= args.months <= 24:
        parser.error("--months must be between 1 and 24")
    try:
        datetime.strptime(args.end_month, "%Y-%m")
    except ValueError:
        parser.error("--end-month must look like 2026-10")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    rows, _ = generate(args.student, args.months, args.end_month)
    out = Path(args.out)
    write_csv(out, rows)
    covered = month_list(args.end_month, args.months)
    first = f"{calendar.month_name[covered[0][1]]} {covered[0][0]}"
    last = f"{calendar.month_name[covered[-1][1]]} {covered[-1][0]}"
    print(f"Wrote {len(rows)} rows ({first} to {last}) to {out}")
    print("This is fake data for practice. Never use your real bank statement.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
