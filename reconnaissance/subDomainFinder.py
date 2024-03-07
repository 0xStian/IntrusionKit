import aiohttp
import asyncio

# max 50 tasks at the same time
semaphore = asyncio.Semaphore(50)

foundSubdomains = []

async def findSubdomains(session, base_domain, subdomain, callback=None):
    async with semaphore:
        subdomain_url = f"http://{subdomain}.{base_domain}"
        try:
            async with session.get(subdomain_url) as response:
                if response.status == 200:
                    foundSubdomains.append(subdomain_url)
                    if callback:
                        callback(subdomain_url)  # Invoke the callback with the found subdomain URL
        except aiohttp.ClientError:
            pass

async def openWordlist(base_domain, wordlist_path, callback=None):
    try:
        with open(wordlist_path, 'r') as wordlist_file:
            subdomains = [word.strip() for word in wordlist_file]
        async with aiohttp.ClientSession() as session:
            tasks = [findSubdomains(session, base_domain, subdomain, callback) for subdomain in subdomains]
            await asyncio.gather(*tasks)
    except Exception as e:
        print(f"Error: {e}")

def start(base_domain, wordlist_path, callback=None):
    foundSubdomains.clear()
    asyncio.run(openWordlist(base_domain, wordlist_path, callback))

