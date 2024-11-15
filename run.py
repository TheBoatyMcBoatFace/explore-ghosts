# run.py
import asyncio
from explorer import hunt_ghosts, logger, configure_logger
from dotenv import load_dotenv

async def main():
    """Main execution function."""
    # Configure the custom logger
    try:
        configure_logger()
        logger.info("🔧 Logger configured successfully.")
    except Exception as e:
        logger.error("❌ Failed to configure logger: %s", str(e))
        return

    # Load environment variables
    try:
        logger.info("🌍 Loading environment variables...")
        load_dotenv()
        logger.info("✅ Environment variables loaded.")
    except Exception as e:
        logger.error("❌ Failed to load environment variables: %s", str(e))
        return

    # Start the hunting process
    try:
        logger.info("👻 Starting the ghost hunt...")
        await hunt_ghosts()
    except Exception as e:
        logger.error("❌ An error occurred in the main execution: %s", str(e))

if __name__ == '__main__':
    try:
        logger.info("🚀 Running the main script!")
        asyncio.run(main())
        logger.info("✅ Script completed successfully!")
    except Exception as e:
        logger.error("❌ Fatal error in script execution: %s", str(e))
