import random
from unittest.mock import Mock, patch

import requests
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import translation

from bookmarks.tests.helpers import BookmarkFactoryMixin
from bookmarks.utils import app_version
from bookmarks.views.settings import get_version_info


class VersionInfoTranslationTestCase(TestCase):
    def test_version_info_is_translated(self):
        response_mock = Mock(status_code=200, json=lambda: {"name": f"v{app_version}"})
        with (
            patch.object(requests, "get", return_value=response_mock),
            translation.override("de"),
        ):
            self.assertEqual(
                get_version_info(random.random()), f"{app_version} (aktuell)"
            )

    def test_version_info_with_newer_version_is_translated(self):
        response_mock = Mock(status_code=200, json=lambda: {"name": "v123.0.1"})
        with (
            patch.object(requests, "get", return_value=response_mock),
            translation.override("de"),
        ):
            self.assertEqual(
                get_version_info(random.random()),
                f"{app_version} (aktuell: 123.0.1)",
            )


class AdminTranslationTestCase(TestCase, BookmarkFactoryMixin):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser("admin", "admin@example.com", "pw")
        self.client.force_login(self.user)

    def test_admin_index_shows_translated_model_names(self):
        response = self.client.get(
            reverse("admin:index"), headers={"accept-language": "de"}
        )
        html = response.content.decode()
        self.assertIn("Lesezeichen", html)
        self.assertIn("Bundles", html)
        self.assertIn("API-Tokens", html)
        self.assertIn("Wartende Aufgaben", html)
        self.assertNotIn("Queued tasks", html)

    def test_admin_bookmark_actions_are_translated(self):
        self.setup_bookmark(user=self.user)
        response = self.client.get(
            reverse("admin:bookmarks_bookmark_changelist"),
            headers={"accept-language": "de"},
        )
        html = response.content.decode()
        self.assertIn("Ausgewählte Lesezeichen archivieren", html)
        self.assertNotIn("Archive selected bookmarks", html)
