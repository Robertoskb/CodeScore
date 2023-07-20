from django.apps import AppConfig


class ExamsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exams'

    def ready(self) -> None:
        import exams.singals  # noqa:401

        return super().ready()
