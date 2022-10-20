from unittest import TestCase, mock
from random import choices

from anu_qrng.clients_free import BLOCK_SIZE, SyncClientFree


class MockResponse:
    def __init__(self, text, status_code):
        self.text = text
        self.status_code = status_code

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def mocked_requests_get_common(*args, **kwargs):
    data = ''.join(choices('01', k=BLOCK_SIZE * 8))
    return MockResponse(data, 200)


class SyncClientFreeTest(TestCase):
    @mock.patch('requests.get', side_effect=mocked_requests_get_common)
    def test_common(self, mock_get):
        client = SyncClientFree()
        data = client.get_random_bytes(10)
        self.assertEqual(len(data), 10)
        mock_get.assert_called_once()

    @mock.patch('requests.get', side_effect=mocked_requests_get_common)
    def test_many(self, mock_get):
        client = SyncClientFree()
        data = client.get_random_bytes(10000)
        self.assertEqual(len(data), 10000)
        self.assertEqual(mock_get.call_count, 79)
