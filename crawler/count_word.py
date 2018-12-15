import asyncio
import aiohttp
import html2text


HANDLE = html2text.HTML2Text()
HANDLE.ignore_links = True


def count_word(word, text):
    return HANDLE.handle(text).count(word)


async def count_one(word, session, url):
    async with session.get(url) as response:
        return count_word(word, await response.text())


async def count_all(word, session, urls):
    all_fetch = [count_one(word, session, url) for url in urls]
    results = await asyncio.gather(*all_fetch, return_exceptions=True)
    return results


async def complete_count(word, urls):
    connector = aiohttp.TCPConnector(limit=100)
    async with aiohttp.ClientSession(connector=connector) as session:
        return await count_all(word, session, urls)


async def main(word, urls):
    result = await complete_count(word, urls)
    return dict(zip(urls, result))
