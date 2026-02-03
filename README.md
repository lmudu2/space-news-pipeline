# Space News Pipeline 🚀

A daily automated data pipeline that fetches the latest space news, performs sentiment analysis, and saves the data for future analysis. This project uses GitHub Actions to run on a daily schedule.

## Features ✨

- **Daily Ingestion**: Automatically fetches top headlines from the [Spaceflight News API](https://api.spaceflightnewsapi.net/v4/docs/).
- **Smart Deduplication**: Tracks processed articles to ensure only unique news is saved, preventing messy duplicates.
- **Sentiment Analysis**: Uses `TextBlob` to analyze the tone of each article (Positive, Neutral, Negative) and assigns a polarity score.
- **Automated Workflow**: Runs automatically every day at 08:00 UTC via GitHub Actions.

## Project Structure 📂

```
.
├── .github/workflows/   # GitHub Actions configuration
├── data/                # Stored JSON data and tracking files
├── ingest_space_news.py # Main logic for fetching and processing news
├── requirements.txt     # Python dependencies
└── README.md            # You are here!
```

## Setup & Usage 🛠️

### Prerequisites
- Python 3.9+
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd <your-repo-name>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   python -m textblob.download_corpora
   ```

### Running Locally

To fetch the latest news and save it to the `data/` folder:

```bash
python ingest_space_news.py
```

Check the `data/` directory for new timestamped JSON files!

## customization ⚙️

- **Change Fetch Limit**: Modify `limit=10` in `ingest_space_news.py` to fetch more or fewer articles.
- **Adjust Schedule**: Edit `.github/workflows/daily_space_news.yml` to change the Cron schedule.

## Future Plans 🔮

- [ ] Daily Markdown Digest generation
- [ ] Email/Slack Notifications
- [ ] Streamlit Dashboard
