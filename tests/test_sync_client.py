from unittest import TestCase, mock
from urllib.parse import urlparse, parse_qs
from random import randbytes

from anu_qrng.clients import API_URL, SyncClient
from anu_qrng.errors import ApiError


API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def mocked_requests_get_common(*args, **kwargs):
    url = args[0]
    parsed = urlparse(url)
    length = int(parse_qs(parsed.query)['length'][0])
    return MockResponse({
        'success': True,
        'data': randbytes(length),
    }, 200)


def mocked_requests_get_error(*args, **kwargs):
    return MockResponse({
        'message': 'Forbidden',
    }, 403)


class SyncClientTest(TestCase):
    @mock.patch('requests.get', side_effect=mocked_requests_get_common)
    def test_common(self, mock_get):
        client = SyncClient(api_key=API_KEY)
        data = client.get_random_bytes(10)
        self.assertEqual(len(data), 10)
        mock_get.assert_called_once_with(
            f'{API_URL}?length=10&type=uint8',
            headers={'x-api-key': API_KEY}
        )

    @mock.patch('requests.get', side_effect=mocked_requests_get_common)
    def test_many(self, mock_get):
        client = SyncClient(api_key=API_KEY)
        data = client.get_random_bytes(10000)
        self.assertEqual(len(data), 10000)
        self.assertEqual(mock_get.call_count, 10)

    @mock.patch('requests.get', side_effect=mocked_requests_get_error)
    def test_error(self, mock_get):
        with self.assertRaisesRegex(ApiError, "Forbidden"):
            client = SyncClient(api_key=API_KEY)
            client.get_random_bytes(10)
        mock_get.assert_called_once_with(
            f'{API_URL}?length=10&type=uint8',
            headers={'x-api-key': API_KEY}
        )
