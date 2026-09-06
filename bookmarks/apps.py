from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BookmarksConfig(AppConfig):
    verbose_name = _("Bookmarks")
    name = "bookmarks"

    def ready(self):
        # Register signal handlers
        # noinspection PyUnusedImports
        import bookmarks.signals  # noqa: F401
