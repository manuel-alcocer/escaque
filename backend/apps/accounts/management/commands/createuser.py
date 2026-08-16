"""Create a trainer account by hand.

Until Google sign-in is wired up this is the only way in:

    python manage.py createuser ana --email ana@example.com
    python manage.py createuser ana --password 's3cret' --display-name 'Ana Ruiz'
    python manage.py createuser admin --superuser

Without --password the command asks for one interactively and never echoes it.
"""

import getpass
import secrets
import string

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

User = get_user_model()

ALPHABET = string.ascii_letters + string.digits


class Command(BaseCommand):
    help = "Create a user account for the chess trainer."

    def add_arguments(self, parser):
        parser.add_argument("username", help="Login name.")
        parser.add_argument("--email", default="", help="Email address.")
        parser.add_argument("--display-name", default="", help="Name shown in the interface.")
        parser.add_argument("--password", help="Password. Prompted for when omitted.")
        parser.add_argument(
            "--generate-password",
            action="store_true",
            help="Generate a random password and print it once.",
        )
        parser.add_argument(
            "--rating",
            type=int,
            default=1200,
            help="Approximate strength, used to order exercises (default: 1200).",
        )
        parser.add_argument("--staff", action="store_true", help="Grant admin site access.")
        parser.add_argument("--superuser", action="store_true", help="Grant full admin rights.")
        parser.add_argument(
            "--skip-password-validation",
            action="store_true",
            help="Accept the password without running Django's validators.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        username = options["username"].strip()
        if not username:
            raise CommandError("The username cannot be empty.")
        if User.objects.filter(username__iexact=username).exists():
            raise CommandError(f"User '{username}' already exists.")

        password, generated = self._resolve_password(options)

        user = User(
            username=username,
            email=options["email"],
            display_name=options["display_name"],
            rating_estimate=options["rating"],
            is_staff=options["staff"] or options["superuser"],
            is_superuser=options["superuser"],
        )

        if not options["skip_password_validation"]:
            try:
                validate_password(password, user)
            except ValidationError as exc:
                raise CommandError(
                    "Password rejected:\n  " + "\n  ".join(exc.messages)
                ) from exc

        user.set_password(password)
        user.save()

        self.stdout.write(self.style.SUCCESS(f"Created user '{user.username}' (id={user.pk})."))
        if generated:
            self.stdout.write(f"Generated password: {password}")
            self.stdout.write(self.style.WARNING("Store it now, it is not shown again."))

    def _resolve_password(self, options) -> tuple[str, bool]:
        if options["generate_password"]:
            return "".join(secrets.choice(ALPHABET) for _ in range(16)), True
        if options["password"]:
            return options["password"], False

        password = getpass.getpass("Password: ")
        confirmation = getpass.getpass("Password (again): ")
        if password != confirmation:
            raise CommandError("The two passwords did not match.")
        if not password:
            raise CommandError("The password cannot be empty.")
        return password, False
