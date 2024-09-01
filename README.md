
# News Scraper for Times of India

This project is a Python-based web scraper designed to extract news articles from the Times of India website. It allows you to scrape a random selection of articles from a specified range of years and save the extracted data (title, date, content, and URL) to a CSV file.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Functionality](#functionality)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Scrape Articles**: Extracts news articles from the Times of India archive pages.
- **Error Handling**: Includes retry mechanisms and error handling to manage network issues and timeouts.
- **Random Article Selection**: Selects random articles to scrape within a specified date range.
- **Save to CSV**: Saves scraped articles to a CSV file for further analysis or use.
- **Progress Bar**: Displays a progress bar to track the scraping process.

## Installation

To use this scraper, you need to have Python installed. Follow the steps below to set up the project:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/news_scraper.git
   cd news_scraper
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the scraper, execute the following command:

```bash
python scraper.py
```

You can modify the parameters such as the range of years and the number of articles to scrape by editing the `scrape_random_articles` function call in the `if __name__ == '__main__':` block.

### Example Usage

```python
scrape_random_articles(2017, 2024, num_articles=10)
```

This example will scrape 10 random articles between the years 2017 and 2024.

## Functionality

### Functions

- **`scrape_archive_page(archive_url, max_retries=3)`**: Scrapes all article links from a single archive page with retries in case of failures.
- **`scrape_article(article_url, max_retries=3)`**: Scrapes the title, content, and date from an individual article page.
- **`scrape_random_articles(start_year, end_year, num_articles=65)`**: Scrapes a random selection of articles from a range of dates.

### How It Works

1. **Scrape Archive Pages**: The script navigates through the Times of India archive pages and extracts article URLs.
2. **Scrape Article Content**: For each article URL, it scrapes the title, content, and date.
3. **Random Selection**: The script selects random articles to ensure a diverse dataset.
4. **Save to CSV**: The scraped data is saved in a CSV file named `times_of_india_articles.csv`.

## Dependencies

The scraper relies on the following Python libraries:

- `requests`: To send HTTP requests to the Times of India server.
- `beautifulsoup4`: To parse and extract information from HTML pages.
- `pandas`: To handle data and save it to a CSV file.
- `tqdm`: To display a progress bar for the scraping process.

Install all dependencies using:

```bash
pip install -r requirements.txt
```

## Contributing

Contributions are welcome! If you have any improvements or new features to suggest, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---


