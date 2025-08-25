```python
     import os
     import scrapy
     from scrapy.crawler import CrawlerProcess
     import logging
     import requests
     from urllib.parse import quote

     # Set up logging
     logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

     class AwesomeSpider(scrapy.Spider):
         name = 'awesome'
         custom_settings = {
             'LOG_LEVEL': 'INFO',
             'USER_AGENT': 'Mozilla/5.0 (compatible; ScrollSurfBot/1.0)',
             'ROBOTSTXT_OBEY': False,
             'DOWNLOAD_DELAY': 2,  # Avoid rate limiting
         }

         def start_requests(self):
             # Use GitHub API for search
             query = quote('awesome list')
             token = os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN')  # Support both
             headers = {'Authorization': f'token {token}'} if token else {}
             url = f'https://api.github.com/search/repositories?q={query}&sort=stars&per_page=10'
             logging.info(f"Starting API request to {url}")
             yield scrapy.Request(url, headers=headers, callback=self.parse_api)

         def parse_api(self, response):
             try:
                 data = response.json()
                 items = data.get('items', [])
                 logging.info(f"Found {len(items)} repositories")
                 for item in items:
                     title = item.get('name', 'Unknown')
                     url = item.get('html_url', '')
                     if title and url:
                         logging.info(f"Yielding: {title}, {url}")
                         yield {'title': title, 'url': url}
             except Exception as e:
                 logging.error(f"Error parsing API response: {e}")

         def closed(self, reason):
             logging.info(f"Spider closed: {reason}")

     if __name__ == '__main__':
         # Ensure output directory exists
         output_dir = 'extension/data'
         os.makedirs(output_dir, exist_ok=True)
         output_file = f'{output_dir}/awesome.txt'
         logging.info(f"Writing to {output_file}")

         # Write dummy data to ensure file creation
         dummy_data = [
             ("Python Resources", "https://github.com/vinta/awesome-python"),
             ("AI Tools", "https://github.com/mlabonne/awesome-ai"),
             ("Web Development", "https://github.com/markodenic/web-development-resources"),
         ]
         try:
             with open(output_file, 'w', encoding='utf-8') as f:
                 for title, url in dummy_data:
                     f.write(f"{title}, {url}\n")
             logging.info(f"Successfully wrote dummy data to {output_file}")
         except Exception as e:
             logging.error(f"Error writing to {output_file}: {e}")

         # Run Scrapy
         try:
             process = CrawlerProcess()
             process.crawl(AwesomeSpider)
             process.start()
         except Exception as e:
             logging.error(f"Error running Scrapy: {e}")
     ```
