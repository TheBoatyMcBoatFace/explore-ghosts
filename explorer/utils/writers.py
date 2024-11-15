# explorer/utils/writers.py
import csv
import asyncio
import os
from .logging import logger

def clean_field(value):
    """Helper function to sanitize text fields by removing line breaks and excessive whitespace."""
    if isinstance(value, str):
        # Remove any newlines and join the text into a single line without excessive spaces
        return ' '.join(value.split())
    return value

async def write_to_csv(data, schema, category):
    """Writes data to a CSV file, including additional fields not in the schema."""
    if data is None:
        logger.warning("⚠️ No data to write.")
        return

    try:
        # Define the output directory as the project root 'output' folder
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        output_dir = os.path.join(project_root, 'output')
        os.makedirs(output_dir, exist_ok=True)

        # Set file path within the root output directory
        file_path = os.path.join(output_dir, f'{category}.csv')

        logger.info("📄 Writing data to CSV file: %s", file_path)

        # Collect schema field names and identify additional fields
        schema_fieldnames = [field['name'] for field in schema]
        schema_ids = [field['id'] for field in schema]

        # Determine additional fields from data keys that aren't in schema_ids
        additional_fieldnames = [
            key for key in data[0].keys() if key not in schema_ids
        ]

        # Combine schema fields and additional fields for the CSV header, ensuring no duplicates
        fieldnames = schema_fieldnames + [field for field in additional_fieldnames if field not in schema_fieldnames]

        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            # Always write the header based on schema and additional fields
            writer.writeheader()
            logger.debug("📝 Writing header to CSV file.")

            # Write rows of data
            for item in data:
                # Clean and remap item fields based on schema, adding any additional fields
                row = {field['name']: clean_field(item.get(field['id'])) for field in schema}

                # Add additional fields to the row without duplicating schema fields, with cleaned data
                additional_data = {key: clean_field(item.get(key)) for key in additional_fieldnames if key not in schema_ids}
                row.update(additional_data)

                writer.writerow(row)

            logger.info(f"✅ Data successfully written to: {file_path}")

    except IOError as e:
        logger.error("❌ IOError while writing to CSV file: %s", str(e))
    except Exception as e:
        logger.error("❌ An unexpected error occurred while writing to CSV: %s", str(e))
