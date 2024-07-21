import httpx
import asyncio


async def fetch_url(url: str) -> int:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.status_code


async def main():
    result_1: asyncio.Task[int] = asyncio.create_task(fetch_url("https://www.google.com"))
    result_2: asyncio.Task[int] = asyncio.create_task(fetch_url("https://www.yahoo.com"))

    print(await result_1)
    print(await result_2)


if __name__ == "__main__":
    asyncio.run(main())
