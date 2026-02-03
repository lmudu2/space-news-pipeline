import requests
import os
import json
from datetime import datetime
from textblob import TextBlob


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

class ProcessingTools:
    @staticmethod
    def analyze_sentiment(text):
        """
        Analyzes the sentiment of the text.
        Returns a tuple of (polarity, sentiment_label).
        Polarity is between -1 (negative) and 1 (positive).
        """
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            label = "Positive"
        elif polarity < -0.1:
            label = "Negative"
        else:
            label = "Neutral"
            
        return polarity, label

class RawDataSaver:
    def __init__(self, folder='data', tracker_file='data/processed_articles.json'):
        self.folder = folder
        self.tracker_file = tracker_file
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        # Load processed IDs
        if os.path.exists(tracker_file):
            with open(tracker_file, 'r') as f:
                self.processed_ids = set(json.load(f))
        else:
            self.processed_ids = set()

    def is_new(self, article_id):
        return str(article_id) not in self.processed_ids

    def save_data(self, articles, filename_prefix='space_news'):
        if not articles:
            return

        # Prepare data for saving (enrich with sentiment)
        enriched_articles = []
        new_ids = []

        for article in articles:
            # Combine title and summary for better sentiment context
            text_to_analyze = f"{article.get('title', '')}. {article.get('summary', '')}"
            polarity, label = ProcessingTools.analyze_sentiment(text_to_analyze)
            
            article['sentiment_score'] = polarity
            article['sentiment_label'] = label
            
            enriched_articles.append(article)
            new_ids.append(str(article['id']))

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{filename_prefix}_{timestamp}.json"
        filepath = os.path.join(self.folder, filename)
        
        with open(filepath, 'w') as f:
            json.dump(enriched_articles, f, indent=4)
        print(f"Saved {len(enriched_articles)} new articles to {filepath}")

        # Update tracker
        self.processed_ids.update(new_ids)
        self._update_tracker()

    def _update_tracker(self):
        with open(self.tracker_file, 'w') as f:
            json.dump(list(self.processed_ids), f)

class IngestionOrchestrator:
    def __init__(self):
        self.client = SpaceFlightClient()
        self.saver = RawDataSaver()

    def ingest(self):
        print("Fetching latest space news articles...")
        articles = self.client.fetch_latest_articles(limit=10)
        
        if articles:
            new_articles = [a for a in articles if self.saver.is_new(a['id'])]
            
            if new_articles:
                print(f"Found {len(new_articles)} new articles. Processing...")
                self.saver.save_data(new_articles)
            else:
                print("No new articles found since last run.")
        else:
            print("No articles fetched. Ingestion aborted.")

if __name__ == "__main__":
    orchestrator = IngestionOrchestrator()
    orchestrator.ingest()
