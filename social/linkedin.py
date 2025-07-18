import requests
import os
from dotenv import load_dotenv

load_dotenv()

def post_linkedin(post_text: str, access_token=None, person_urn=None):
    access_token = access_token or os.getenv("LINKEDIN_ACCESS_TOKEN")
    person_urn = person_urn or os.getenv("LINKEDIN_PERSON_URN")


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

def post_linkedin_poll(
    post_text: str,
    poll_question: str,
    poll_options: list[str],
    poll_duration_days: int = 7,
    access_token=None,
    author_urn=None
):
    """
    Post a poll to LinkedIn using the new Posts API.

    Args:
        post_text (str): Commentary for the post
        poll_question (str): The poll's question (max 140 chars recommended)
        poll_options (list[str]): A list of 2-4 option strings (each max 30 chars)
        poll_duration_days (int): Duration in days (1, 3, 7, or 14)
        access_token (str): OAuth2 access token
        author_urn (str): The URN of the user/org posting (e.g., "urn:li:person:xxx")
    Returns:
        bool: True if post succeeds, False otherwise
    """

    # API requires string values for duration: ONE_DAY, THREE_DAYS, etc.
    duration_map = {1: "ONE_DAY", 3: "THREE_DAYS", 7: "SEVEN_DAYS", 14: "FOURTEEN_DAYS"}
    duration_str = duration_map.get(poll_duration_days, "SEVEN_DAYS")

    access_token = access_token or os.getenv("LINKEDIN_ACCESS_TOKEN")
    author_urn = author_urn or os.getenv("LINKEDIN_PERSON_URN")

    url = "https://api.linkedin.com/rest/posts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "LinkedIn-Version": "202306",  # Use latest supported, e.g. "202506"
        "X-Restli-Protocol-Version": "2.0.0"
    }

    # Format poll options (LinkedIn allows 2-4 options, text <= 30 chars each)
    poll_options_formatted = [{"text": opt[:30]} for opt in poll_options[:4]]

    data = {
        "author": author_urn,
        "commentary": post_text[:1300],  # commentary has a limit (typically 1300 chars)
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": []
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
        "content": {
            "poll": {
                "question": poll_question[:140],
                "options": poll_options_formatted,
                "settings": {
                    "duration": duration_str
                }
            }
        }
    }

    resp = requests.post(url, headers=headers, json=data)

    print("LinkedIn poll post status:", resp.status_code)
    if resp.content:
        try:
            print("Response:", resp.json())
        except Exception:
            print("Response is not JSON:", resp.text)
    else:
        print("No content in response.")

    return resp.status_code in (200, 201)
