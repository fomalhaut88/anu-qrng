import asyncio

import aiohttp
import requests

from .errors import ApiError


API_URL = "https://api.quantumnumbers.anu.edu.au"
MAX_SIZE = 1024


class AsyncClient:
    def __init__(self, api_key, api_url=API_URL):
        self._api_key = api_key
        self._api_url = api_url

    async def _get_random_array(self, size, type_='uint8'):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self._api_url}?length={size}&type={type_}",
                                   headers={'x-api-key': self._api_key}) as resp:
                result = await resp.json()
                if result['success']:
                    return result['data']
                else:
                    raise ApiError(result['message'])

    async def get_random_bytes(self, size):
        coro_list = []
        while size > 0:
            sz = min(size, MAX_SIZE)
            coro = self._get_random_array(sz, type_='uint8')
            coro_list.append(coro)
            size -= sz
        arr_list = await asyncio.gather(*coro_list)
        return b''.join(map(bytes, arr_list))


class SyncClient:
    def __init__(self, api_key, api_url=API_URL):
        self._api_key = api_key
        self._api_url = api_url

    def _get_random_array(self, size, type_='uint8'):
        with requests.get(f"{self._api_url}?length={size}&type={type_}",
                          headers={'x-api-key': self._api_key}) as resp:
            result = resp.json()
            if result['success']:
                return result['data']
            else:
                raise ApiError(result['message'])

    def get_random_bytes(self, size):
        arr_list = []
        while size > 0:
            sz = min(size, MAX_SIZE)
            arr = self._get_random_array(sz, type_='uint8')
            arr_list.append(arr)
            size -= sz
        return b''.join(map(bytes, arr_list))
