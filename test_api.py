import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com/posts"


@pytest.fixture
def new_post():
    """Fixture that returns a valid post dictionary."""
    return {
        "title": "foo",
        "body": "bar",
        "userId": 1
    }


def test_create_post(new_post):
    """Test to create a new post and verify it was created successfully."""
    response = requests.post(BASE_URL, json=new_post)
    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
    data = response.json()
    assert data["title"] == new_post["title"], f"Expected title to be {new_post['title']}, got {data['title']}"
    assert data["body"] == new_post["body"], f"Expected body to be {new_post['body']}, got {data['body']}"
    assert data["userId"] == new_post["userId"], f"Expected userId to be {new_post['userId']}, got {data['userId']}"


def test_get_posts():
    """Test to retrieve all posts and verify the response is a non-empty list."""
    response = requests.get(BASE_URL)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    data = response.json()
    assert isinstance(data, list), f"Expected a list, got {type(data)}"
    assert len(data) > 0, "Expected at least one post, got none"


def test_update_post():
    """Test to update an existing post and verify the update was successful."""
    update_data = {
        "title": "updated title",
        "body": "updated body",
        "userId": 1
    }
    response = requests.put(f"{BASE_URL}/1", json=update_data)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    data = response.json()
    assert data["title"] == update_data["title"], f"Expected title to be {update_data['title']}, got {data['title']}"
    assert data["body"] == update_data["body"], f"Expected body to be {update_data['body']}, got {data['body']}"
    assert data["userId"] == update_data[
        "userId"], f"Expected userId to be {update_data['userId']}, got {data['userId']}"


def test_delete_post():
    """Test to delete an existing post and verify the deletion was successful."""
    response = requests.delete(f"{BASE_URL}/1")
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    data = response.json()
    assert data == {}, f"Expected an empty response body, got {data}"


def test_create_post_missing_fields():
    """Negative test: Attempt to create a post with missing required fields and verify the error response."""
    incomplete_post = {"title": "foo"}
    response = requests.post(BASE_URL, json=incomplete_post)
    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"


def test_get_non_existent_post():
    """Negative test: Attempt to retrieve a non-existent post and verify the error response."""
    response = requests.get(f"{BASE_URL}/9999")
    assert response.status_code == 404, f"Expected status code 404, got {response.status_code}"


def test_update_post_invalid_data():
    """Negative test: Attempt to update a post with invalid data and verify the error response."""
    invalid_data = {"title": 123, "body": "cat", "userId": 5678}
    response = requests.put(f"{BASE_URL}/1", json=invalid_data)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    data = response.json()
    assert isinstance(data['title'], int), "Expected title to be a string"
    assert isinstance(data['body'], str), "Expected body to be a string"
    assert isinstance(data['userId'], int), "Expected userId to be an integer"

