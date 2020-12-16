def get_auth_header(client, username="test", password="test"):
    response = client.post("/login", json=dict(username=username, password=password))

    access_token = response.json["access_token"]

    return {"Authorization": f"Bearer {access_token}"}


def add_test_book(client):
    client.post(
        "/book",
        json=dict(
            title="A Test Book",
            author="Some Author",
            publisher="Some Publisher",
            pages=1000,
        ),
        headers=get_auth_header(client),
    )


def test_index(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json["application"] == "Flask Example API"


def test_get_book(client):
    add_test_book(client)
    response = client.get(
        "/book/A%20Test%20Book",
        headers=get_auth_header(client),
    )

    assert response.status_code == 200


def test_book_not_found(client):
    response = client.get(
        "/book/UnknownBook",
        headers=get_auth_header(client),
    )

    assert response.status_code == 404


def test_add_book(client):
    response = client.post(
        "/book",
        json=dict(
            title="Some Book",
            author="Some Author",
            publisher="Some Publisher",
            pages=1000,
        ),
        headers=get_auth_header(client),
    )

    assert response.status_code == 200


def test_update_book(client):
    response = client.put(
        "/book",
        json=dict(
            title="Some Book",
            author="Some Author",
            publisher="Some Publisher",
            pages=1000,
        ),
        headers=get_auth_header(client),
    )

    assert response.status_code == 201


def test_delete_book(client):
    response = client.delete(
        "/book/Some%20Book",
        headers=get_auth_header(client),
    )

    assert response.status_code == 200