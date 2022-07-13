def test_response_ok(api_client):
    response = api_client.get("/")
    # TODO: This is a sample test.
    #       We may create better tests for the next developments.
    assert response.status_code == 200
