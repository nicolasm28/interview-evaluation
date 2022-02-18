import factory
from app.schemas import TodoPayload, UserPayload


class UserFactory(factory.Factory):
    name = factory.Faker("name")
    email = factory.Faker("email")
    username = factory.Faker("user_name")
    password = factory.Faker("pystr")

    class Meta:
        model = UserPayload


class ItemFactory(factory.Factory):
    title = factory.Faker("sentence")
    body = factory.Faker("paragraph")

    class Meta:
        model = TodoPayload