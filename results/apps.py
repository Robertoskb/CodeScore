from django.apps import AppConfig


class ResultsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'results'

    def ready(self) -> None:
        import results.singals  # noqa:401

        return super().ready()
