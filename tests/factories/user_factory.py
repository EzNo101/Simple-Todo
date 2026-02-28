import factory
from app.schemas.user import UserCreate

class UserFactory(factory.Factory):
    class Meta:
        model = UserCreate
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    password = factory.LazyFunction(lambda: "12345678")