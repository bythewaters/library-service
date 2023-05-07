from django.test import TestCase
from library_service import settings
from unittest.mock import patch
from notifications.telegram_notification import send_to_telegram


class TelegramTestCase(TestCase):
    @patch("requests.post")
    def test_send_to_telegram(self, requests_post_mock):
        # Arrange
        message = "Test message"
        chat_id = "test_chat_id"
        api_token = "test_api_token"
        settings.TELEGRAM_CHAT_ID = chat_id
        settings.TELEGRAM_API_TOKEN = api_token
        expected_url = f"https://api.telegram.org/bot{api_token}/sendMessage"
        expected_data = {"chat_id": chat_id, "text": message}

        # Act
        send_to_telegram(message)

        # Assert
        requests_post_mock.assert_called_once_with(expected_url, json=expected_data)
