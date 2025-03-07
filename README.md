
# Streamlined Web Scraping

## Overview
This Python-based solution facilitates efficient extraction and categorisation of links from web pages. It processes a given CSV file containing domain URLs, fetches metadata (title and description), categorises links based on predefined patterns, and outputs the results to a new CSV file.

The project is ideal for handling large datasets or for scraping multiple web pages to gather insights and categorise URLs for further analysis. The code is designed to be scalable, leveraging `ThreadPoolExecutor` for concurrent processing to ensure fast execution even for extensive lists of domains.

## Features
- **Concurrent Fetching**: Utilises `ThreadPoolExecutor` to fetch metadata from links concurrently for fast processing.
- **Link Categorisation**: Automatically categorises URLs into predefined categories (e.g., "Contact Us", "About Us", "Services", etc.) based on URL patterns.
- **Metadata Extraction**: Retrieves titles and descriptions from webpages to enrich the scraped data.
- **CSV Input and Output**: Handles input and output in CSV format for easy integration into data pipelines and analyses.

## Prerequisites
- Python 3.7+
- Required Python libraries:
  - `requests`
  - `pandas`
  - `beautifulsoup4`
  - `re`
  - `urllib.parse`
  
You can install the required libraries using `pip`:
```bash
pip install requests pandas beautifulsoup4
```

## Usage

### Input
The script expects a CSV file containing domain URLs (one per row). For example, `input.csv` should have a structure like:

| URL |
| --- |
| http://example.com |
| https://anotherexample.com |

### Output
The results will be saved to a CSV file with the following columns:
- `Input URL`: The domain URL from the input CSV.
- `Extracted URL`: The actual URL found on the page.
- `Category`: The category assigned to the link based on predefined patterns.
- `Title`: The title of the webpage.
- `Metadata`: The description metadata of the webpage.

### Running the Script
To run the script, ensure that you have replaced the placeholders for input and output file paths:

```python
fetch_links("path_to_your_input_file.csv", "path_to_your_output_file.csv")
```

Make sure to replace `path_to_your_input_file.csv` and `path_to_your_output_file.csv` with actual file paths.

### Notes
- Ensure your input CSV does not contain any extraneous characters and has a valid list of domain URLs.
- This script fetches metadata from the first page of each domain URL and attempts to categorise all the links found within it.
- If a domain page fails to load, it will be marked with `Failed to fetch` in the output.

## Code Details

- **Categorisation Logic**: The script uses regular expressions to match URLs against predefined patterns. Each pattern is associated with a category (e.g., "Services", "Contact Us").
- **Concurrency**: The script uses `ThreadPoolExecutor` to perform parallel processing for fetching link metadata, making it scalable for large datasets.
- **Error Handling**: Basic error handling is implemented to skip failed domains or links that cannot be processed.

## Example

Input CSV (`input.csv`):
```
https://example.com
http://anotherexample.com
```

Output CSV (`output.csv`):
```
Input URL, Extracted URL, Category, Title, Metadata
https://example.com, https://example.com/contact, Contact Us, Example Contact Page, "Contact us for more information"
https://anotherexample.com, https://anotherexample.com/about, About Us, About Us - Another Example, "Learn more about us"
```

## Contributing
Feel free to fork the repository, submit issues, or open pull requests. Contributions and suggestions are always welcome!
