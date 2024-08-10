from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Zotero FastAPI application"}

def test_create_item():
    response = client.post("/items/", json={
        "itemType": "book",
        "title": "Test Book",
        "abstractNote": "Test Abstract",
        "creators": [{"creatorType": "author", "primary": True}],
        "tags": [{"tag": "test"}],
        "notes": [{"note": "test note"}],
        "dateAdded": "2024-07-31T00:00:00Z",
        "dateModified": "2024-07-31T00:00:00Z"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"
