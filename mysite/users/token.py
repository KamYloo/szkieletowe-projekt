from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class TokenGenerator(PasswordResetTokenGenerator):
    """
        Generator tokenów do aktywacji konta użytkownika.

        Działa na podstawie identyfikatora użytkownika, znacznika czasu
        oraz informacji o aktywności użytkownika.

    """

    def _make_hash_value(self, user, timestamp):
        """
                Tworzy wartość hasha dla generowania tokena.

                Argumenty:
                    user (User): Użytkownik, dla którego tworzony jest token.
                    timestamp (int): Znacznik czasu.

                Zwraca:
                    str: Wartość hasha używana do generowania tokena.

        """

        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

# Instancja generatora tokenów do aktywacji konta użytkownika
account_activation_token = TokenGenerator()