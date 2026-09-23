from django.contrib.auth import get_user_model
from django.db import transaction

from accounts.models import Profile


User = get_user_model()

class UserService:

    @staticmethod
    @transaction.atomic()
    def create_user_with_profile(
        *,
        username,
        email,
        password,
        name,
        mobile_phone,
    ):
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        Profile.objects.create(
            user=user,
            name=name,
            mobile_phone=mobile_phone,
        )

        return user