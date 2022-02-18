from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class BaseTodo(BaseModel):
    title: str = Field(..., description="A title for the task.")
    body: Optional[str] = Field(
        None,
        description="A detailed description of the task.",
    )

    # orm_mode will tell the Pydantic model to read the data even if it is not a dict
    class Config:
        orm_mode = True


class TodoItem(BaseTodo):
    """A task to do."""

    id: int = Field(..., description="The item unique ID.")
    completed: bool = Field(
        ..., description="Indicates if this task has been completed."
    )
    username: Optional[str] = Field(
        ...,
        description="The user who created this item.",
    )

    # orm_mode will tell the Pydantic model to read the data even if it is not a dict
    class Config:
        orm_mode = True

class TodoPayload(BaseTodo):
    """Data for the item being created."""

class BaseUser(BaseModel):
    name: str
    email: EmailStr
    username: str

    # orm_mode will tell the Pydantic model to read the data even if it is not a dict
    class Config:
        orm_mode = True

class UserPayload(BaseUser):
    password: str

class User(BaseUser):
    pass

class StoredUser(BaseUser):
    password_hash: str
