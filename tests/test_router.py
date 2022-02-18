import pydantic
import pytest
from app.schemas import TodoItem, User, UserPayload
from fastapi import FastAPI
from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth
from . import factories


@pytest.fixture()
def fastapi_app():
    from app.router import router

    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture()
def client(fastapi_app: FastAPI):
    with TestClient(fastapi_app) as client:
        return client


@pytest.fixture()
def valid_credentials(client: TestClient):
    payload: UserPayload = factories.UserFactory()
    response = client.post(
        url="/users/",
        json=payload.dict(
            by_alias=True,
            exclude_unset=True,
        ),
    )
    assert response.status_code == 201
    return HTTPBasicAuth(payload.username, payload.password)


@pytest.fixture()
def invalid_credentials():
    payload = factories.UserFactory()
    return HTTPBasicAuth(payload.username, payload.password)

@pytest.fixture()
def existing_item(client: TestClient, valid_credentials: HTTPBasicAuth):
    response = client.post(
        url="/items/",
        json=factories.ItemFactory().dict(by_alias=True, exclude_unset=True),
        # addingccredentials to create a new item - POST
        auth= valid_credentials
    )
    return pydantic.parse_obj_as(TodoItem, response.json())

@pytest.fixture()
def existing_user(client: TestClient):
    payload: UserPayload = factories.UserFactory()
    response = client.post(
        url= '/users/',
        json= payload.dict(by_alias= True,exclude_unset=True),
    )
    assert response.status_code == 201
    return HTTPBasicAuth(payload.username, payload.password)


class TestAuthentication:
    def test_creates_user(self, client: TestClient):
        payload: UserPayload = factories.UserFactory()
        response = client.post(
            url="/users/",
            json=payload.dict(
                by_alias=True,
                exclude_unset=True,
            ),
        )
        assert response.status_code == 201
        user = pydantic.parse_obj_as(User, response.json())
        assert user.username == payload.username

    def test_returns_valid_user(
        self,
        client: TestClient,
        valid_credentials: HTTPBasicAuth,
    ):
        response = client.get("/users/me", auth=valid_credentials)
        assert response.status_code == 200
        user = pydantic.parse_obj_as(User, response.json())
        assert user.username == valid_credentials.username

    def test_returns_401_without_credentials(self, client: TestClient):
        response = client.get("/users/me")
        assert response.status_code == 401

    def test_returns_401_with_invalid_credentials(
        self, client: TestClient, invalid_credentials: HTTPBasicAuth
    ):
        response = client.get("/users/me", auth=invalid_credentials)
        assert response.status_code == 401



class TestItemCrud:
    def test_returns_401(self, client: TestClient):
        response = client.post(
            url="/items/",
            json=factories.ItemFactory().dict(
                by_alias=True,
                exclude_unset=True,
            ),
        )
        assert response.status_code == 401

    def test_returns_newly_created_item(
        self,
        client: TestClient,
        valid_credentials: HTTPBasicAuth,
    ):
        payload = factories.ItemFactory()
        response = client.post(
            url="/items/",
            json=payload.dict(
                by_alias=True,
                exclude_unset=True,
            ),
            auth=valid_credentials,
        )
        assert response.status_code == 201
        todo = pydantic.parse_obj_as(TodoItem, response.json())
        assert todo.id is not None
        assert not todo.completed
        assert todo.username == valid_credentials.username

    def test_returns_the_item(
        self, client: TestClient, existing_item: TodoItem,
    ):
        response = client.get(f"/items/{existing_item.id}")
        assert response.status_code == 200
        response_item = pydantic.parse_obj_as(TodoItem, response.json())
        assert response_item == existing_item

    '''
    TODO: Add missing tests
    
    @router.put("/items/{id}"
    Ensure the user is authenticated. If not, either return a 401 response
    or raise an `HttpException` with a 401 code.
    '''
    def test_ensure_user_is_auth_while_put(
        self,
        client: TestClient,
        existing_item: TodoItem
        ):
        
        payload = factories.ItemFactory()
        
        response = client.put(
            url= f'/items/{existing_item.id}',
            json= {
                "title": payload.title,
                "body": payload.body
                })
        
        assert response.status_code == 401

    '''
    @router.put("/items/{id}"
    Check the username matches the item's username. 
    Check status_code is 200 when success.
    '''
    def test_username_matches_item_user_put(
        self,
        client: TestClient,
        existing_item: TodoItem,
        valid_credentials: HTTPBasicAuth,
        existing_user: HTTPBasicAuth
        ):
        
        payload = factories.ItemFactory()
        response = client.put(
            url= f'/items/{existing_item.id}',
            json= {
                "title": payload.title,
                "body": payload.body
                },
            auth= valid_credentials
        )
    
        assert valid_credentials.username == existing_item.username
        assert response.status_code == 200

        '''
        If not, return a 403 - Fesponse or raise a `HttpException` with a 403 code.
        '''
        response_invalid_user = client.put(
            url= f'/items/{existing_item.id}',
            json= {
                "title": payload.title,
                "body": payload.body
                },
            auth= existing_user
        )
        assert response_invalid_user.status_code == 403
    
    '''
    @router.delete("/items/{id}"
    Ensure the user is authenticated.
    '''
    def test_user_is_auth_while_delete(
        self,
        client: TestClient,
        existing_item: TodoItem
        ):
               
        response = client.delete(
            url= f'/items/{existing_item.id}')
        
        assert response.status_code == 401

    '''
    @router.put("/items/{id}"
    Check if the currently logged username matches.
    Verify success while removing the item from the store.  
    '''
    def test_username_matches_item_user_delete(
        self,
        client: TestClient,
        existing_item: TodoItem,
        valid_credentials: HTTPBasicAuth,
        ):
        
        response = client.delete(
            url= f'/items/{existing_item.id}',
            auth= valid_credentials
        )
    
        assert valid_credentials.username == existing_item.username
        assert response.status_code == 200

        response_deleted_item = client.get(
            url= f'/items/{existing_item.id}'
        )

        assert response_deleted_item.status_code == 204
    