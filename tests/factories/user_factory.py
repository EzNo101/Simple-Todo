import factory

from app.schemas.user import UserCreate

class UserFactory(factory.Factory):
    class Meta:
        model = UserCreate
    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.LazyFunction(lambda: "12345678")