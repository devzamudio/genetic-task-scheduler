from app import create_app


def test_cors_allows_frontend_origin_for_scenario_uploads():
    app = create_app()
    client = app.test_client()

    response = client.options(
        "/api/v1/scenarios",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type",
        },
    )

    assert response.status_code == 200
    assert response.headers.get("Access-Control-Allow-Origin") == "http://localhost:5173"
    assert "POST" in response.headers.get("Access-Control-Allow-Methods", "")
