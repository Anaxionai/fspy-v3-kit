"""Quick checks that the starter is set up: the API imports, has ReelPipe's routes, and lets
the web app call it. They pass from day one and need no emulator.
"""

from app.main import app
from fastapi.testclient import TestClient


def test_api_has_reelpipe_routes():
    routes = {(method, route.path) for route in app.routes for method in getattr(route, "methods", ())}
    assert ("POST", "/uploads") in routes
    assert ("POST", "/uploads/{video_id}/complete") in routes
    assert ("GET", "/videos") in routes
    assert ("GET", "/videos/{video_id}") in routes


def test_cors_lets_the_web_app_call_the_api():
    client = TestClient(app)
    response = client.options(
        "/uploads",
        headers={"Origin": "http://localhost:5173", "Access-Control-Request-Method": "POST"},
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"
