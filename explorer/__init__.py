# explorer/__init__.py
import asyncio
from .utils import logger, load_yaml_config, write_to_csv, configure_logger
from .page_scraping import scroll_and_scrape, init_web_driver
from .find_explorers import get_explore_pages
from .fetcher import fetch_page

async def hunt_ghosts():
    logger.info("🔄 Starting the main process...")

    # Load the configuration file
    config = load_yaml_config('config.yml')
    sitemap_url = config.get('sitemap_url')
    ignore_categories = set(config.get('ignore', []))
    category_mapping = config.get('category_mapping', {})

    # Fetch explore pages using sitemap URL
    if sitemap_url:
        explore_pages = get_explore_pages(sitemap_url)
        logger.info(f"🔗 Retrieved {len(explore_pages)} explore pages from sitemap.")
    else:
        logger.error("❌ Sitemap URL not provided in config.")
        return

    # Initialize the web driver
    browser, page = await init_web_driver()
    if browser is None or page is None:
        logger.error("❌ Web driver initialization failed.")
        return

    try:
        # Process each explore page
        for explore_url in explore_pages:
            # Extract everything after "/explore/" as the category slug
            if '/explore/' in explore_url:
                category_slug = explore_url.split('/explore/')[-1].strip('/')

                # Skip if category_slug is empty or in the ignore list
                if not category_slug or category_slug in ignore_categories:
                    logger.info(f"⏩ Skipping category '{category_slug}' as per ignore settings.")
                    continue

                logger.info(f"🗂️ Processing explore category: {category_slug}")

            else:
                logger.warning(f"⚠️ URL does not contain /explore/: {explore_url}")
                continue

            # Pagination through pages for the current category
            page_number = 0
            category_items = []
            while True:
                logger.info(f"🗂️ Fetching page {page_number} for category '{category_slug}'...")

                # Pass category_mapping here
                items = await fetch_page(page_number, category_slug, category_mapping)
                if not items:
                    logger.info(f"🔚 No more items found for page {page_number} in category '{category_slug}'.")
                    break

                category_items.extend(items)
                page_number += 1

            # Use the schema for remapping data before saving
            data = await scroll_and_scrape(config, category_items)
            if data:
                # Write CSV file immediately after processing the category
                file_name = category_slug.replace(" & ", "_").replace(" ", "_").lower()
                await write_to_csv(data, config.get('schema', []), file_name)
                logger.info(f"💾 Data for category '{category_slug}' written to CSV as '{file_name}.csv'")
            else:
                logger.warning(f"🚫 No data found to save for category '{category_slug}'.")

        logger.info("✨ Crawl process completed successfully!")

    except Exception as e:
        logger.error("❌ An error occurred during the crawling process: %s", str(e))

    finally:
        await browser.close()
        logger.info("🛑 Browser closed.")
