from django.apps import AppConfig

class ProfilesAppConfig(AppConfig):
    # Specifies the default primary key type for models in this app
    default_auto_field = 'django.db.models.BigAutoField'

    # Defines the name of the app used by Django
    name = 'profiles_app'
