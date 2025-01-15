"""Validators module."""

import re

import phonenumbers
import validators
from phonenumbers import NumberParseException, geocoder


class Validators:
    """Validators class."""

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate an email address."""
        if not email:
            return False

        # Validate email format
        if not validators.email(email):
            return False

        # List of known disposable email domains
        disposable_domains = {
            "mailinator.com",
            "10minutemail.com",
            "temp-mail.org",
            "yopmail.com",
            "guerrillamail.com",
            "discardmail.com",
            "maildrop.cc",
            "fakeinbox.com",
            "getnada.com",
            "temp.com",
            "test.com",
            "test1.com",
            "test2.com",
            "temp1.com",
            "temp2.com",
        }

        # Extract domain from email
        domain = email.split("@")[1].lower()
        if domain in disposable_domains:
            return False

        # Check for common dummy patterns
        dummy_patterns = [
            r"^test@",
            r"^dummy@",
            r"^fake@",
            r"^no-reply@",
            r"^temp@",
            r"^trial@",
            r"^trial1@",
            r"^temp1@",
            r"^temp2@",
            r"^example@",
            r"^[a-zA-Z]@[a-zA-Z]\.[a-zA-Z]{2,}$",
        ]
        if any(re.match(pattern, email) for pattern in dummy_patterns):
            return False

        return True

    @staticmethod
    def validate_name(name: str) -> bool:
        """Validate a name (first or last name)."""
        if not name:
            return False
        # Regex to match valid names (letters, spaces, hyphens, apostrophes)
        name_pattern = r"^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$"
        if not re.match(name_pattern, name):
            return False
        if len(name) < 2 or len(name) > 20:
            return False
        return True

    @staticmethod
    def is_valid_phonenumber(phone_number: str) -> bool:
        """Validate a phone number."""
        try:
            parsed_number = phonenumbers.parse(phone_number, "GH")
            if not phonenumbers.is_valid_number(parsed_number):
                return False

            if geocoder.description_for_number(parsed_number, "en") != "Ghana":
                return False

            return True
        except NumberParseException:
            return False
