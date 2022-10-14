# anu-qrng

This Python library implements an interface to interact with quantum random generator service [ANU QRNG](https://qrng.anu.edu.au/). It supports the documented API (https://quantumnumbers.anu.edu.au/documentation) that is efficient and requires `API_KEY` that you can get from https://quantumnumbers.anu.edu.au/api-key (if you are logged in). Also you can try free clients that do not require `API_KEY` and request https://qrng.anu.edu.au instead. But it is a slower and unpleasant way.

## Installation

```
pip install git+ssh://git@github.com/fomalhaut88/anu-qrng.git
```

## Example

```python
import asyncio

from anu_qrng.clients import AsyncClient, SyncClient
from anu_qrng.clients_free import  AsyncClientFree, SyncClientFree


# Take it here: https://quantumnumbers.anu.edu.au/api-key
API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


async def main():
    # Asynchronous client (it uses https://api.quantumnumbers.anu.edu.au)
    client = AsyncClient(api_key=API_KEY)
    print(await client.get_random_bytes(10))

    # Synchronous client (it uses https://api.quantumnumbers.anu.edu.au)
    client = SyncClient(api_key=API_KEY)
    print(client.get_random_bytes(10))

    # Free asynchronous client (it uses https://qrng.anu.edu.au)
    client = AsyncClientFree()
    print(await client.get_random_bytes(10))

    # Free synchronous client (it uses https://qrng.anu.edu.au)
    client = SyncClientFree()
    print(client.get_random_bytes(10))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```
