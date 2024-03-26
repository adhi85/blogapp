from fastapi.testclient import TestClient
import sys
import os
from fastapi import status

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app

client = TestClient(app)

sample_blog_data ={
  "title": "Sample blog about Cloud applications",
  "body": "AWS is a cloud platform",
  "tags": [
    "cloud",
    "tech"
  ],
  "owner_id": "65facef09ae7082531f0cf30",
  "created_at": "2024-03-20 11:58:02",
  "updated_at": "2024-03-20 11:58:02"
}

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Blogs API. Visit /docs for documentation."}


# def test_create_blog():
#     response = client.post("/api/blogs/", json=sample_blog_data)
#     assert response.status_code == status.HTTP_201_CREATED
#     assert response.json() == {"message": "Blog created successfully"}

def test_read_all_blogs():
    response = client.get("/api/blogs/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

# def test_read_non_existing_blog():
#     response = client.get("/non_existing_id")
#     assert response.status_code == status.HTTP_404_NOT_FOUND
#     assert response.json()["detail"] == "Blog not found"