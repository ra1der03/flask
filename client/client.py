import asyncio
import aiohttp


async def main():
    client = aiohttp.ClientSession()

    response = await client.get(
        "http://127.0.0.1:8080/advertisement/1",
        # json={'name': 'True', 'description': 'just a True', 'owner': 'George'}
    )

    # response = await client.get("http://127.0.0.1:8080/advertisement/1")

    data = await response.text()
    print(data)
    await client.close()


asyncio.run(main())

