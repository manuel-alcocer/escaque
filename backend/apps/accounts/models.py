from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user.

    Accounts are created by hand with `manage.py createuser`. The Google fields are
    already here so social sign-in can be plugged in later without a data migration:
    an OIDC callback only needs to fill `google_sub` on an existing user.
    """

    display_name = models.CharField(
        max_length=80,
        blank=True,
        help_text="Name shown in the interface. Falls back to the username.",
    )
    google_sub = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        db_index=True,
        help_text="Google OpenID Connect subject identifier. Empty until the account is linked.",
    )
    rating_estimate = models.PositiveIntegerField(
        default=1200,
        help_text="Rough self-declared strength, used to order exercises by difficulty.",
    )
    board_orientation_hint = models.CharField(
        max_length=5,
        choices=[("white", "White"), ("black", "Black"), ("auto", "Auto")],
        default="auto",
        help_text="Preferred board orientation when it is not forced by the exercise.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta(AbstractUser.Meta):
        db_table = "accounts_user"

    def __str__(self):
        return self.username

    @property
    def name(self) -> str:
        return self.display_name or self.username
