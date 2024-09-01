import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import calendar
import time
from datetime import datetime
from tqdm import tqdm

# Base URL for the Times of India archive page (use the newspaper needed)
BASE_URL = 'https://timesofindia.indiatimes.com/archivelist/year-{year},month-{month},starttime-{starttime}.cms'

def scrape_archive_page(archive_url, max_retries=3):
  """Scrape all article links from a single archive page with retries. | find the tags from the webpages (inspect)"""
  retries = 0
  while retries < max_retries:
    try:
      response = requests.get(archive_url, timeout=15)  # Increased timeout
      if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        articles = []
        for row in soup.find_all('tr', class_='rightColWrap'):
          a_tag = row.find('a', href=True)
          if a_tag:
            url = a_tag['href']
            if not url.startswith('http'):
              url = 'https://timesofindia.indiatimes.com' + url
            articles.append(url)

        return articles
      else:
        print(f"Failed to retrieve archive page {archive_url} with status code {response.status_code}")
        return []
    except Exception as e:
      print(f"An error occurred while scraping archive page {archive_url}: {e}")
      retries += 1
      time.sleep(random.uniform(2, 5))  # Increased sleep time and randomization
  print(f"Max retries reached for {archive_url}. Skipping...")
  return []  # Return empty list after max retries

def scrape_article(article_url, max_retries=3):
  """Scrape the title, content, and date from an article page with retries."""
  retries = 0
  while retries < max_retries:
    try:
      response = requests.get(article_url, timeout=20)  # Increased timeout
      soup = BeautifulSoup(response.content, 'html.parser')

      # Extract the article title
      title_tag = soup.find('h1', {'class': 'HNMDR'})
      title = title_tag.text.strip() if title_tag else 'No Title'

      # Extract the article content
      content_div = soup.find('div', {'class': '_s30J clearfix'})
      content = content_div.get_text(separator=' ', strip=True) if content_div else 'No Content'

      # Extract the publication date
      byline_div = soup.find('div', {'class': 'xf8Pm byline'})
      date_span = byline_div.find('span') if byline_div else None
      date = date_span.text.strip() if date_span else 'No Date'

      return {'url': article_url, 'title': title, 'date': date, 'content': content}
    except Exception as e:
      print(f"An error occurred while scraping article {article_url}: {e}")
      retries += 1
      time.sleep(random.uniform(2, 5))  # Increased sleep time and randomization
  print(f"Max retries reached for {article_url}. Skipping...")
  return {'url': article_url, 'title': 'Error', 'date': 'Error', 'content': 'Error'}

def scrape_random_articles(start_year, end_year, num_articles=65):
  """Scrape a random selection of articles from a range of dates."""
  all_articles = []
  processed_urls = set()
  max_attempts = 1000

  with tqdm(total=num_articles, desc="Scraping articles") as progress_bar:
    attempts = 0
    while len(all_articles) < num_articles and attempts < max_attempts:
      year = random.randint(start_year, end_year)
      month = random.randint(1, 12)
      days_in_month = calendar.monthrange(year, month)[1]
      day = random.randint(1, days_in_month)
      date = datetime(year, month, day)

      # Correct starttime calculation
      starttime = (date - datetime(1899, 12, 30)).days

      # Construct the correct archive URL
      archive_url = BASE_URL.format(year=year, month=month, starttime=starttime)
      print(f"Scraping archive page: {archive_url}")

      article_links = scrape_archive_page(archive_url)

      if not article_links:
        print(f"No articles found for {archive_url}")
        attempts += 1
        continue

      random.shuffle(article_links)  # Shuffle to ensure random selection

      for article_url in article_links:
        if article_url not in processed_urls:
          processed_urls.add(article_url)
          article_data = scrape_article(article_url)
          all_articles.append(article_data)
          print(f"Scraped article: {article_data['title']}")
          progress_bar.update(1)  # Update the progress bar
          if len(all_articles) >= num_articles:
            break

      attempts += 1
      if len(all_articles) < num_articles:
        print("Sleeping before the next request...")
        time.sleep(random.uniform(1, 3))  # Sleep to avoid overwhelming the server

  # Save results to CSV
  print("Saving results to CSV...")
  df = pd.DataFrame(all_articles)
  df.to_csv('times_of_india_articles.csv', columns=['title', 'date', 'content', 'url'], index=False)
  print("Scraping complete. Results saved to 'times_of_india_articles.csv'.")

if __name__ == '__main__':
  scrape_random_articles(2017, 2024, num_articles=10)