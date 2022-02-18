from typing import List
from fastapi import APIRouter, Response, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .schemas import TodoItem, TodoPayload, User, UserPayload, BaseUser
from .statements import get_items, get_item, create_item, update_item, delete_item, get_user, create_user
from .dependencies import authentication, get_db
import re
from passlib.hash import sha256_crypt

router = APIRouter()

@router.get("/items/", response_model=List[TodoItem])
def items(db: Session = Depends(get_db)):
    """Retrieve a persistent list of items."""

    items = get_items(db)
    
    # if None is returned, then no data has been obtained -> empty table
    if len(items) != 0:
        return items
    else:
        return Response(status_code= status.HTTP_204_NO_CONTENT)


@router.get("/items/{id}", response_model=TodoItem)
def item(id: int, db: Session = Depends(get_db)):
    """Retrieve a particular item from the store."""
    item = get_item(db, id)
    
    # if None is returned, then no data has been obtained -> inexistant item
    if item != None:
        return item
    else:
        return Response(status_code= status.HTTP_204_NO_CONTENT)


@router.post(
    path="/items/",
    response_model=TodoItem,
    status_code=201,
    response_description="The item has been created successfully.",
)
def new_item(
    payload: TodoPayload,
    db: Session = Depends(get_db),
    username: str = Depends(authentication)):

    """Add an item to the store."""
    try:
        # Adding username to item.
        return create_item(db, payload, username)
    
    # catching error
    except Exception as e:
        return JSONResponse({'error': str(e)})
    

@router.put("/items/{id}", response_model=TodoItem)
def put_item(
    id: int,
    payload: TodoPayload,
    db: Session = Depends(get_db),
    username: str = Depends(authentication)):
    
    # Ensure that the item is stored already in the datastore. 
    item = get_item(db, id)

    if item != None:
        # Check the username matches the item's username. If not, return a 403
        # response or raise a `HttpException` with a 403 code.
        if item.username != username:
            raise HTTPException(
                status_code= status.HTTP_403_FORBIDDEN,
                detail= "username does not match"
            )
        else:
            # updating item in our database
            return update_item(db, id, payload)
    else:
        # if not, raise an `HttpException` with a 404 code or return a 404 response.
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="inexistant ID"
        )

@router.delete("/items/{id}", 
    response_class=Response, 
    status_code=204)
def remove_item(
    id: int,
    db: Session = Depends(get_db),
    username: str = Depends(authentication)):

    item = get_item(db, id)

    if item != None:
        # Check the username matches the item's username. If not, return a 403
        # response or raise a `HttpException` with a 403 code.
        if item.username != username:
            raise HTTPException(
                status_code= status.HTTP_403_FORBIDDEN,
                detail= "username does not match"
            )
        else:
            # deleting item from our database
            delete_item(db, id)
            return JSONResponse({'result': 'item deleted'})

    else:
        # if not, raise an `HttpException` with a 404 code or return a 404 response.
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="inexistant ID"
        )


@router.post(path= "/users/",
    response_model= BaseUser,
    status_code=201,
    response_description="User has been created successfully.")
def new_user(payload: UserPayload,
    db: Session = Depends(get_db)):
    
    user = get_user(db, payload.username)

    # validating user
    if user != None:
        return JSONResponse({'error': 'user already exist'})
    else:
        # 1. Validate the username has no uppercase letter, @ sign, nor punctuations.
        username = payload.username
        if re.search('[@]', username):
            return JSONResponse({'error': 'username cannot contain @'})
        elif re.search('[A-Z]', username):
            return JSONResponse({'error': 'username cannot contain uppercases'})
        elif re.search('''[!"',-./:;?_]''', username):
            return JSONResponse({'error': 'username cannot contain punctuations'})

    # hashing pwd
    pwd = payload.password
    pwd_hashed = sha256_crypt.hash(pwd)
    
    # storing user in our db
    return create_user(db, 
        payload,
        pwd_hashed)

'''
TODO: Document this endpoint
Get current user already authenticated.
Verify if the user has valid credentials thru Authentication dependency;
    if not, then status_code HTTP_401_UNAUTHORIZED will be returned.
    while sucess the endpoint will be returning User model.
'''
@router.get(
    path="/users/me",
    response_model= User
    )
def get_current_user(
    # 1. Get the credentials from the request.
    # 3. Validate the password.
    username: str = Depends(authentication),
    db: Session = Depends(get_db)):

    #  2. Retrieve the user by it's username from the store.
    #  4. Return the user without the password hash.
    return get_user(db, username)
