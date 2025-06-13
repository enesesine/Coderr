from django.apps import AppConfig

# This class configures the 'auth_app' Django application
class AuthAppConfig(AppConfig):
    # Specifies the default type for auto-incrementing primary keys (BigAutoField)
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Defines the name of the application, which must match the folder name
    name = 'auth_app'
