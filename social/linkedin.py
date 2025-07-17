import requests
import os
from dotenv import load_dotenv

load_dotenv()

def post_linkedin(post_text: str):
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    person_urn = os.getenv("LINKEDIN_PERSON_URN")

    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    data = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": post_text},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    resp = requests.post(url, headers=headers, json=data)
    print("Response status:", resp.status_code)
    print("Response body:", resp.text)
    return resp.status_code == 201

def post_linkedin_poll(post_text: str, poll_question: str, poll_options: list[str], poll_duration_days: int = 7):
    access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    person_urn = os.getenv("LINKEDIN_PERSON_URN")

    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    poll_options_formatted = [{"text": opt[:30]} for opt in poll_options[:4]]

    data = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": post_text},
                "shareMediaCategory": "POLL",
                "poll": {
                    "question": poll_question[:100],
                    "options": poll_options_formatted,
                    "pollDuration": poll_duration_days
                }
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }

    resp = requests.post(url, headers=headers, json=data)
    print("LinkedIn poll post status:", resp.status_code)
    print("Response:", resp.text)
    return resp.status_code == 201
