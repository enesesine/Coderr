from django.apps import AppConfig

class OffersAppConfig(AppConfig):
    """
    Configuration class for the offers_app Django application.

    This is used by Django to set up the app and define metadata such as
    its name and the default type of auto-created primary keys.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Use BigAutoField for primary keys by default
    name = 'offers_app'  # Name of the app as used in INSTALLED_APPS and imports
