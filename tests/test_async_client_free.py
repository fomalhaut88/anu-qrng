from unittest import IsolatedAsyncioTestCase, mock
from random import choices

from anu_qrng.clients_free import BLOCK_SIZE, AsyncClientFree


class MockResponse:
    def __init__(self, text_data, status):
        self.text_data = text_data
        self.status = status

    async def text(self):
        return self.text_data

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


class MockClientSession:
    def __init__(self, text_data, status):
        self.text_data = text_data
        self.status = status

    def get(self, *args, **kwargs):
        return MockResponse(self.text_data, self.status)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


def mocked_session_common(*args, **kwargs):
    data = ''.join(choices('01', k=BLOCK_SIZE * 8))
    return MockClientSession(data, 200)


def mocked_session_error(*args, **kwargs):
    return MockClientSession({
        'message': 'Forbidden',
    }, 403)


class AsyncClientFreeTest(IsolatedAsyncioTestCase):
    @mock.patch('aiohttp.ClientSession', side_effect=mocked_session_common)
    async def test_common(self, mock_session):
        client = AsyncClientFree()
        data = await client.get_random_bytes(10)
        self.assertEqual(len(data), 10)
        mock_session.assert_called_once()

    @mock.patch('aiohttp.ClientSession', side_effect=mocked_session_common)
    async def test_many(self, mock_session):
        client = AsyncClientFree()
        data = await client.get_random_bytes(10000)
        self.assertEqual(len(data), 10000)
        self.assertEqual(mock_session.call_count, 79)
