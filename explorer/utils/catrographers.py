# explorer/utils/cartographers.py
import yaml
from .logging import logger

def remap_data(data, schema):
    """Remap data fields according to the schema and add new fields to the end."""
    logger.info("🔄 Starting data remapping process.")
    mapped_data = []
    schema_ids = [s['id'] for s in schema]

    for item in data:
        try:
            mapped_item = {}
            # Map fields according to schema
            for field in schema:
                field_name = field['name']
                field_id = field['id']
                mapped_item[field_name] = item.get(field_id, None)
                logger.debug(f"🗺️ Mapped field '{field_name}' with id '{field_id}' to value '{mapped_item[field_name]}'")

            # Add any additional fields
            additional_fields = {key: item[key] for key in item if key not in schema_ids}
            mapped_item.update(additional_fields)
            logger.debug("📝 Additional fields added: %s", additional_fields)

            mapped_data.append(mapped_item)
        except KeyError as e:
            logger.warning("⚠️ Missing expected field in item data: %s", str(e))
        except Exception as e:
            logger.error("❌ Error processing item in remapping: %s", str(e))

    logger.info("✅ Data remapping completed. Total items remapped: %d", len(mapped_data))
    return mapped_data
