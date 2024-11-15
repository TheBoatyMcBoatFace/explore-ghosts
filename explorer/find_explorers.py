# explorer/find_explorers.py
import requests
import xml.etree.ElementTree as ET
from .utils import logger

def get_explore_pages(sitemap_url):
    """Fetches explore pages from the sitemap."""
    logger.info("🌐 Fetching sitemap from %s", sitemap_url)

    try:
        # Fetch the sitemap
        response = requests.get(sitemap_url)
        response.raise_for_status()
        logger.info("✅ Sitemap fetched successfully.")

        # Try parsing the XML content
        try:
            root = ET.fromstring(response.content)
            logger.info("🌲 XML content parsed successfully.")
        except ET.ParseError as e:
            logger.error("❌ XML parsing error: %s", e)
            return []

        # Define the namespace and find the explore pages
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        explore_pages = [
            url.text for url in root.findall('ns:url/ns:loc', namespace)
            if '/explore/' in url.text
        ]

        # Extract category names from URLs (everything after "/explore/")
        categories = [page.split('/explore/')[-1].strip('/') for page in explore_pages]

        # Log the number and list of categories found
        logger.info("🔗 Found %d explore pages (categories) in the sitemap:", len(categories))

        # Log each category name, one per row
        if categories:
            logger.info("🌐 List of explore categories:\n" + "\n".join(categories))

        return explore_pages

    # Handle different types of requests-related errors
    except requests.exceptions.HTTPError as e:
        logger.error("❌ HTTP error occurred while fetching the sitemap: %s", e)
    except requests.exceptions.ConnectionError as e:
        logger.error("⚠️ Connection error while accessing the sitemap: %s", e)
    except requests.exceptions.Timeout as e:
        logger.error("⏳ Timeout error while fetching the sitemap: %s", e)
    except requests.exceptions.RequestException as e:
        logger.error("❌ Failed to fetch sitemap: %s", e)

    logger.warning("🚫 No explore pages found due to an error.")
    return []
