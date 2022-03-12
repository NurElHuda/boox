import factory
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save


@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "boox_app.User"
        django_get_or_create = ("email",)

    username = factory.Sequence(lambda n: f"user_{n}")
    name = factory.Sequence(lambda n: f"user_{n}")
    email = factory.Sequence(lambda n: f"user_{n}@mail.com")
    password = (make_password("p"),)


@factory.django.mute_signals(post_save)
class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "boox_app.Book"

    title = factory.Sequence(lambda n: f"book_{n}")