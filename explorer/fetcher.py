# explorer/fetcher.py
import os
import aiohttp
import json
from urllib.parse import quote
from .utils import logger

# Fetching sensitive values from environment variables
SUPER_SECRET_URL = os.getenv('SUPER_SECRET_URL')
SUPER_SECRET_PARAMS_1 = os.getenv('SUPER_SECRET_PARAMS_1')
SUPER_SECRET_PARAMS_2 = os.getenv('SUPER_SECRET_PARAMS_2')
SUPER_SECRET_PARAMS_3 = os.getenv('SUPER_SECRET_PARAMS_3')

async def fetch_page(page_number, category, category_mapping):
    """Fetch data for a given page number and category using fetcher logic."""

    if not SUPER_SECRET_URL:
        logger.error("🚨 Missing SUPER_SECRET_URL in environment variables!")
        return None

    # Use the category mapping if available, fall back to original category if not
    full_category_name = category_mapping.get(category, category)

    # URL-encode the full category name to handle special characters (e.g., spaces, '&', etc.)
    encoded_category = quote(full_category_name)

    logger.info(f"🌐 Preparing to fetch data for page {page_number} in category '{full_category_name}' (encoded: '{encoded_category}')...")

    async with aiohttp.ClientSession() as session:
        url = f"{SUPER_SECRET_URL}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0',
            'content-type': 'application/x-www-form-urlencoded',
        }

        # Dynamically construct the payload with encoded category name
        payload = {
            "requests": [
                {
                    "indexName": "EXPLORE",
                    "params": (
                        f"{SUPER_SECRET_PARAMS_1}{encoded_category}"
                        f"{SUPER_SECRET_PARAMS_2}{page_number}"
                        f"{SUPER_SECRET_PARAMS_3}"
                    )
                }
            ]
        }

        logger.debug(f"👀 Payload being sent for category '{category}' on page {page_number}: {json.dumps(payload, indent=2)}")

        try:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status != 200:
                    logger.error(f"❌ Failed to fetch page {page_number} for category '{category}': Status {response.status}")
                    return None

                logger.info("📥 Successfully received response, parsing JSON...")
                data = await response.json()

                # Log a sample of the fetched data for debugging purposes
                logger.debug(f"🕵️ Sample data for page {page_number} and category '{category}': {json.dumps(data['results'][0]['hits'][:2], indent=2)}")

                return data['results'][0]['hits']

        except aiohttp.ClientError as e:
            logger.error(f"⚠️ HTTP client error for page {page_number} and category '{category}': {str(e)}")
        except json.JSONDecodeError as e:
            logger.error(f"⚠️ JSON decode error for page {page_number} in category '{category}': {str(e)}")
        except Exception as e:
            logger.error(f"❌ Unexpected error: {str(e)}")

    logger.warning(f"🚫 No data returned for page {page_number} in category '{category}'")
    return None
