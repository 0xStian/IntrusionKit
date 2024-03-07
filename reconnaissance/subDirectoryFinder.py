import aiohttp
import asyncio
import urllib.parse




# max 50 tasks at the same time
semaphore = asyncio.Semaphore(50)

foundSubdirectories = []

async def findSubdirectories(session, url, word):
    async with semaphore:
        subdirectory_url = urllib.parse.urljoin(url, word)
        async with session.get(subdirectory_url) as response:
            if response.status == 200 and "404" not in await response.text():
                print("[+] Discovered subdirectory: " + subdirectory_url)
                foundSubdirectories.append(subdirectory_url)

async def openWordlist(url, wordlist_path):
    try:
        with open(wordlist_path, 'r') as wordlist_file:
            words = [word.strip() for word in wordlist_file]
        async with aiohttp.ClientSession() as session:
            tasks = [findSubdirectories(session, url, word) for word in words]
            await asyncio.gather(*tasks)
    except:
        pass

def start(url, wordlist_path):
    foundSubdirectories.clear()
    asyncio.run(openWordlist(url, wordlist_path))
    return foundSubdirectories