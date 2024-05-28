from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
        Tworzy profil użytkownika po zapisaniu nowego użytkownika.

        Argumenty:
            sender (Model): Klasa modelu, która wysyła sygnał.
            instance (User): Instancja modelu User, która została zapisana.
            created (bool): Określa, czy instancja została właśnie utworzona.

    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
        Zapisuje profil użytkownika po zapisaniu instancji użytkownika.

        Argumenty:
            sender (Model): Klasa modelu, która wysyła sygnał.
            instance (User): Instancja modelu User, która została zapisana.

    """

    instance.profile.save()
