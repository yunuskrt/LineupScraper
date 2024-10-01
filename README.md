# Lineup Scraper

## Project Overview

The **Lineup Scraper** is a web scraping and ETL (Extract, Transform, Load) project that fetches data from [Transfermarkt](https://www.transfermarkt.com/). It collects and processes data related to matches, players, teams, and managers, and associates them within a database. This project is structured to download, parse, transform, and load data into MongoDB.

## Table of Contents

- Project Overview
- Data Collection & Extraction
- Data Transformation
- Data Loading
- File Descriptions

## Data Collection & Extraction

The data collection phase is handled in several steps:

1. **download_links.py**: Fetches and stores links to the data source in a file.
2. **save_html_pages.py**: Reads the saved links and downloads the corresponding HTML pages to local storage.
3. **parse_html.py**: Parses the saved HTML pages and converts them into a structured JSON format.
4. **check_exists.py**: Ensures all downloaded links have been parsed successfully.
5. **check_parsed_data.py**: Validates that the parsed data matches the expected structure and format.

## Data Transformation

After extraction, the data undergoes transformation to prepare it for storage:

1. **combine_full_data.py**: Aggregates data across all leagues and iterates over matches to combine them into a single JSON file.
2. **write_non_relational.py**: Prepares the JSON files that are suitable for insertion into MongoDB. Ensures data associations, consistency of IDs, etc.
3. **check_non_relational.py**: Verifies that the transformed data adheres to the structure required for MongoDB storage.
4. **download_image_links.py**: Extracts all image links and stores them in a file.
5. **save_images.py**: Downloads and saves player/manager/team images locally.

## Data Loading

- The parsed and transformed data is stored in MongoDB.
- The **db/mongo/app.js** file contains logic for inserting data and handling all database interactions using Node.js.

## File Descriptions

- **config.py**: Configuration file containing paths for files to read/write.
- **download_links.py**: Script to download and save links for scraping.
- **save_html_pages.py**: Downloads HTML pages from the previously saved links.
- **parse_html.py**: Parses HTML files and extracts data into JSON format.
- **check_exists.py**: Verifies if all downloaded links have corresponding parsed data.
- **check_parsed_data.py**: Checks if parsed data is in the correct format.
- **combine_full_data.py**: Aggregates all match data into a single file.
- **write_non_relational.py**: Prepares the JSON files for MongoDB insertion, maintaining data consistency and relationships.
- **check_non_relational.py**: Validates the structure of JSON data before inserting it into MongoDB.
- **download_image_links.py**: Gathers image links for players and managers.
- **save_images.py**: Downloads images and stores them in the specified folder.
- **db/mongo/app.js**: Node.js script to insert transformed data into MongoDB.
