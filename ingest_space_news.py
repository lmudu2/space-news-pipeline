import requests
import os
import json
from datetime import datetime


class SpaceFlightClient:
    def __init__(self, base_url='https://api.spaceflightnewsapi.net/v4/articles'):
        self.base_url = base_url
    def fetch_latest_articles(self, limit=10):
        response = requests.get(f"{self.base_url}?limit={limit}")
        if response.status_code == 200:
            return response.json()['results']
        else:
            print(f"Failed to fetch articles: {response.status_code}")
            return []
class RawDataSaver:
    def __init__(self, folder='data'):
        self.folder = folder
        if not os.path.exists(folder):
            os.makedirs(folder)
    def save_raw_data(self, data, filename_prefix='space_news'):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{filename_prefix}_{timestamp}.json"
        filepath = os.path.join(self.folder, filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Raw data saved to {filepath}")
class IngestionOrchestrator:
    def __init__(self):
        self.client = SpaceFlightClient()
        self.saver = RawDataSaver()
    def ingest(self):
        print("Fetching latest space news articles...")
        articles = self.client.fetch_latest_articles(limit=10)
        if articles:
            print(f"Fetched {len(articles)} articles. Saving raw data...")
            self.saver.save_raw_data(articles)
        else:
            print("No articles fetched. Ingestion aborted.")

if __name__ == "__main__":
    orchestrator = IngestionOrchestrator()
    orchestrator.ingest()
