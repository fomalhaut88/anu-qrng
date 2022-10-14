import time
import math
import asyncio

import aiohttp
import requests

from .errors import ApiError


URL_TEMPLATE = "https://qrng.anu.edu.au/wp-content/plugins/colours-plugin/get_block_binary.php?_={tsm}"
BLOCK_SIZE = 128


class AsyncClientFree:
    async def _get_random_block(self, tsm):
        url = URL_TEMPLATE.format(tsm=tsm)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.text()
                    return int(data, 2).to_bytes(BLOCK_SIZE, byteorder='big')
                else:
                    raise ApiError(await resp.text())

    async def get_random_bytes(self, size):
        ts = time.time()
        tsm = int(ts * 1000)
        coro_list = [
            self._get_random_block(tsm + i)
            for i in range(math.ceil(size / BLOCK_SIZE))
        ]
        block_list = await asyncio.gather(*coro_list)
        return b''.join(map(bytes, block_list))[:size]


class SyncClientFree:
    def _get_random_block(self, tsm):
        url = URL_TEMPLATE.format(tsm=tsm)

        with requests.get(url) as resp:
            if resp.status_code == 200:
                return int(resp.text, 2).to_bytes(BLOCK_SIZE, byteorder='big')
            else:
                raise ApiError(resp.text)

    def get_random_bytes(self, size):
        ts = time.time()
        tsm = int(ts * 1000)
        block_list = []
        for i in range(math.ceil(size / BLOCK_SIZE)):
            block = self._get_random_block(tsm + i)
            block_list.append(block)
        return b''.join(map(bytes, block_list))[:size]
