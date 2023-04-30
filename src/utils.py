import aiohttp
import json
from config import bitlyToken

async def constrain_text_to_length(text, length):
    result = text
    if len(result) > length:
        result = f"{result[:length]}..."
    return result

async def shorten_link(link):
    url = 'https://api-ssl.bitly.com/v4/shorten'
    data = {
        "long_url": link
    }
    headers = {
        'Authorization': f"Bearer {bitlyToken}",
        'Content-Type': 'application/json'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=json.dumps(data), headers=headers) as resp:
            if resp.status in range(200, 299):
                response_data = await resp.json()
                short_link = response_data.get('link', '')
                if short_link:
                    return short_link
                else:
                    return None
            else:
                print(f"Bitly error: {resp.status}: {resp.reason}")
                return None
