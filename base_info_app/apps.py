from django.apps import AppConfig

class BaseInfoAppConfig(AppConfig):
    """
    Configuration class for the 'base_info_app' application.
    
    This class sets default configurations for the app, such as:
    - The default auto field used for model primary keys.
    - The name of the app as recognized by Django.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base_info_app'
