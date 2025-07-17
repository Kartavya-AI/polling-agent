import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

def post_tweet(text: str, consumer_key=None, consumer_secret=None, access_token=None, access_token_secret=None):
    client = tweepy.Client(
        consumer_key=consumer_key or os.getenv("TWITTER_CONSUMER_KEY"),
        consumer_secret=consumer_secret or os.getenv("TWITTER_CONSUMER_SECRET"),
        access_token=access_token or os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=access_token_secret or os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    )
    response = client.create_tweet(text=text)
    return response.data.get("id")

def post_poll(text: str, options: list, duration_minutes: int = 1440, consumer_key=None, consumer_secret=None, access_token=None, access_token_secret=None):
    client = tweepy.Client(
        consumer_key=consumer_key or os.getenv("TWITTER_CONSUMER_KEY"),
        consumer_secret=consumer_secret or os.getenv("TWITTER_CONSUMER_SECRET"),
        access_token=access_token or os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=access_token_secret or os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    )

    response = client.create_tweet(
        text=text,
        poll_options=options,
        poll_duration_minutes=duration_minutes
    )
    return response.data.get("id")
