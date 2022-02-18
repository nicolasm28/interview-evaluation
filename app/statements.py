from .models import Todo, Users
from sqlalchemy.exc import IntegrityError

def get_items(db):
    return db.query(Todo).all()

def get_item(db, _id):
    return db.query(Todo).filter(Todo.id == _id).first()

def create_item(db, item, _username):
    db_item = Todo(
        title= item.title,
        body= item.body,
        completed= False,
        username= _username
    )
    # catching error while performing INSERT
    try:
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except IntegrityError as e: 
        raise Exception(e.orig)

def create_user(db, user, _pwd_hashed):
    new_user = Users(
        name= user.name,
        email= user.email,
        username= user.username,
        pwd_hashed= _pwd_hashed
    )
    # catching error while performing INSERT
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as e: 
        raise Exception(e.orig)

def get_user(db, _username):
    return db.query(Users).filter(Users.username == _username).first()

def get_pwd(db, _username):
    return db.query(Users).filter(Users.username == _username).first()

def update_item(db, _id, payload):    
    db.query(Todo).filter(Todo.id == _id).\
        update(
            {Todo.title: payload.title,
            Todo.body: payload.body},
            synchronize_session=False)
    db.commit()
    return get_item(db, _id)

def delete_item(db, _id):
    db.query(Todo).filter(Todo.id == _id).\
        delete(synchronize_session=False)
    db.commit()
    return True
