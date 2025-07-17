from pydantic import BaseModel
from typing import List, Optional


class TwitterPost(BaseModel):
    tweet_text: str


class TwitterPoll(BaseModel):
    tweet_text: str
    poll_question: str
    poll_options: List[str]


class LinkedInPoll(BaseModel):
    post_text: str
    poll_question: str
    poll_options: List[str]


class PollsOutput(BaseModel):
    Twitter_Poll: TwitterPoll
    LinkedIn_Poll: LinkedInPoll


class LinkedInPost(BaseModel):
    post_text: str