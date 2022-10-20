from unittest import IsolatedAsyncioTestCase, mock
from random import randbytes
from urllib.parse import urlparse, parse_qs

from anu_qrng.clients import AsyncClient
from anu_qrng.errors import ApiError


API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


class MockResponse:
    def __init__(self, json_data, status):
        self.json_data = json_data
        self.status = status

    async def json(self):
        return self.json_data

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


class MockClientSession:
    def __init__(self, json_data, status, use_length_from_url=False):
        self.json_data = json_data
        self.status = status
        self.use_length_from_url = use_length_from_url

    def get(self, *args, **kwargs):
        if self.use_length_from_url:
            url = args[0]
            parsed = urlparse(url)
            length = int(parse_qs(parsed.query)['length'][0])
            self.json_data['data'] = randbytes(length)
        return MockResponse(self.json_data, self.status)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


def mocked_session_common(*args, **kwargs):
    return MockClientSession({
        'success': True,
        'data': b'',
    }, 200, use_length_from_url=True)


def mocked_session_error(*args, **kwargs):
    return MockClientSession({
        'message': 'Forbidden',
    }, 403)


class AsyncClientTest(IsolatedAsyncioTestCase):
    @mock.patch('aiohttp.ClientSession', side_effect=mocked_session_common)
    async def test_common(self, mock_session):
        client = AsyncClient(api_key=API_KEY)
        data = await client.get_random_bytes(10)
        self.assertEqual(len(data), 10)
        mock_session.assert_called_once()

    @mock.patch('aiohttp.ClientSession', side_effect=mocked_session_common)
    async def test_many(self, mock_session):
        client = AsyncClient(api_key=API_KEY)
        data = await client.get_random_bytes(10000)
        self.assertEqual(len(data), 10000)
        self.assertEqual(mock_session.call_count, 10)

    @mock.patch('aiohttp.ClientSession', side_effect=mocked_session_error)
    async def test_error(self, mock_session):
        with self.assertRaisesRegex(ApiError, "Forbidden"):
            client = AsyncClient(api_key=API_KEY)
            await client.get_random_bytes(10)
        mock_session.assert_called_once()
