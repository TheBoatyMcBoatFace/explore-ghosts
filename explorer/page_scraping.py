# explorer/page_scraping.py
import asyncio
from pyppeteer import launch
from .utils import logger, remap_data

async def init_web_driver():
    """Initialize and return the browser and page instance."""
    try:
        logger.info("🚗 Initializing WebDriver...")

        # This path is provided by the GitHub Action that installs Chrome
        chrome_path = '/usr/bin/google-chrome'

        browser = await launch(
            headless=True,
            executablePath=chrome_path,  # Use system-installed Chrome
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
            ]
        )
        page = await browser.newPage()
        logger.info("✅ WebDriver initialized successfully.")
        return browser, page

    except Exception as e:
        logger.error(f"❌ Failed to initialize WebDriver: {str(e)}")
        return None, None

async def scroll_and_scrape(config, total_items):
    """Scrape data based on configuration and list of items."""
    logger.info("🔍 Starting the scroll and scrape process.")

    schema = config.get('schema', [])
    schema_ids = [s['id'] for s in schema]
    data_list = []

    for item in total_items:
        try:
            # Map fields from schema and additional data
            mapped_item = {field['name']: item.get(field['id']) for field in schema}
            additional_fields = {k: v for k, v in item.items() if k not in schema_ids}
            mapped_item.update(additional_fields)
            data_list.append(mapped_item)
            logger.debug("📝 Mapped item: %s", mapped_item)
        except KeyError as e:
            logger.warning("⚠️ Missing field in item data: %s", str(e))
        except Exception as e:
            logger.error("❌ Error processing item: %s", str(e))

    if not data_list:
        logger.warning("⚠️ No data scraped.")
        return None

    logger.info("✅ Completed scraping. Data collected for %d items.", len(data_list))
    return data_list
