import factory
from accountapp.models import CustomUser, Profile

# https://faker.readthedocs.io/en/stable/providers.html
faker = factory.Faker("ko_KR")


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Sequence(lambda n: "testuser{}".format(n))
    password = factory.PostGenerationMethodCall("set_password", "z1x2c3a4")


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    nickname = factory.Sequence(lambda n: "nick{}".format(n))
    avatar = None
    email = factory.Sequence(lambda n: "testuser{}@example.org".format(n))
