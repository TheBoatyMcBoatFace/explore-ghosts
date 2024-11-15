# Explore Ghosts: Ghost Explore Site Scraper

[![Run Ghost Explorer](https://github.com/TheBoatyMcBoatFace/explore-ghosts/actions/workflows/get_ghosts.yml/badge.svg)](https://github.com/TheBoatyMcBoatFace/explore-ghosts/actions/workflows/get_ghosts.yml)   [![Bob Yeets Whale (Docker Image)](https://github.com/TheBoatyMcBoatFace/explore-ghosts/actions/workflows/build_puppet.yml/badge.svg)](https://github.com/TheBoatyMcBoatFace/explore-ghosts/actions/workflows/build_puppet.yml)

A project designed to pull down all of the sites listed on Ghost's Explore platform and save them in various formats (csv, json, yaml, sqlite, etc.). This project is designed to help track Ghost websites and potentially monitor trends over time, making it ideal for anyone looking to analyze Ghost websites or track growth and movement.

**To view Ghost Explore, head over to [ghost.org](https://ghost.org/explore?utm_source=TheBoatyMcBoatFace/explore-ghosts&utm_medium=github).

### Project Goals:
1. **Nightly Scraping**: Scrapes all the sites featured on Ghost Explore and saves the results in various formats (CSV, JSON, YAML, and more).
2. **Tracking & Trend Analysis**: Enables future features for tracking Ghost website rankings as they increase or decrease over time.
3. **Storage Solutions**: Potential integrations with external databases for long-term storage (e.g., Clickhouse or DoltHub) to maintain a large history of websites and metric data.
4. **Open Source Contribution**: Encourages the open-source community to enhance the scraping process, post-processing, and ultimately enable powerful analytics.


## Getting Started

You need `Python` and [`Poetry`](https://python-poetry.org/) installed.

### Steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/theboatymcboatface/explore-ghosts.git
   cd explore-ghosts
   ```

2. Install the dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Create an **`.env`** file (see below for explanation of environment variables):
   ```bash
   cp .env-template .env
   ```

4. Update your `config.yml` and `.env` configuration as needed.

5. Run `poetry run python run.py`
This script will:
- Connect to the Ghost Explore platform.
- Pull down all listed Ghost websites.
- Save the results according to your configuration (e.g., as CSV, JSON, etc.).

## Configuration

The scraper relies on the **`config.yml`** file to control how data is mapped, explore pages are fetched, and behavior is configured. Here's a breakdown of its contents:

### `config.yml`
- **sitemap_url**: The base sitemap URL used to retrieve explore pages (currently pointing to Ghost Explore).
- **load_wait**: Waiting period in seconds for page loads (not always needed).
- **ignore**: A list of explore categories to ignore.
- **category_mapping**: Maps URL slugs to more readable or complete category names, that may contain special characters.

Example:

```yaml
# config.yml
sitemap_url: https://ghost.org/sitemap-pages.xml
load_wait: 0.5

ignore:
  - about
  - featured
  - revenue

category_mapping:
  health: Health & Wellness
  faith: Faith & Spirituality
  sport: Sport & Fitness
  nature: Nature & Outdoors
  food: Food & Drink
  house: House & Home
  fashion: Fashion & Beauty
  gear: Gear & Gadgets
```

---

### Environmental Variables

The `.env` file contains the variables required to configure logging, output options, and API secrets. You REALLY should look at this...


## File Structure

Here's a brief overview of the project's file structure:

```
.
├── config.yml               # Configuration for input considerations, category mappings, etc.
├── explorer/                # Core logic for scraping and saving files
│   ├── fetcher.py           # Used to fetch data from Ghost's public API
│   ├── utils/               # Logging, file writers, config loaders, and helpers
│   └── page_scraping.py     # Scraping logic and web driver interaction
├── output/                  # Output directory for CSV, YAML, JSON, or other files
└── run.py                   # The main entry point that runs the process
```

---

## Upcoming Features / TODO:

- **Output Types**: We still need to fully enable multiple file format outputs (YAML, JSON, SQLite).
- **GitHub Actions**: Automate the running of this scraper to run nightly as a scheduled task on GitHub Actions (Cron Jobs). The generated output should be committed back to the same repository.
- **Data Analysis & Visualization**: Add scripts to analyze trends over time (e.g., site growth) and create Markdown reports that get committed back to the repo.
- **Database Integration**: Explore potential integration with external databases (e.g., **Clickhouse**) or cloud storage providers like DoltHub to store history.



## License

This project is licensed under the AGPL-3.0 License, like everything else I do. You can learn about the AGPL license [here](https://www.gnu.org/licenses/agpl-3.0.en.html).

```text
Explore Ghosts is freely available for anyone to use and modify. However, if you make improvements or alterations, you're encouraged to contribute them back to the community to help foster collaborative growth.
```

---

## Contributing

Contributions are welcome! Please feel free to submit issues, pull requests, or feature requests.

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/my-new-feature`.
3. Make your changes.
4. Commit your changes: `git commit -am 'Add some feature'`.
5. Push to the branch: `git push origin feature/my-new-feature`.
6. Submit a pull request 🎉.

Looking forward to your ideas and contributions! If you need any support or just want to discuss improvements, feel free to reach out!


**I hate creating READMEs, so this file was shamelessly generated using AI**
