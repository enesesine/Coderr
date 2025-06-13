from django.apps import AppConfig

# Configuration class for the reviews_app Django application
class ReviewsAppConfig(AppConfig):
    # Specifies the type of primary key field to use for models in this app by default
    default_auto_field = 'django.db.models.BigAutoField'

    # Name of the app — used by Django to identify it
    name = 'reviews_app'
