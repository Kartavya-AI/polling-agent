import streamlit as st
import json
import os
from datetime import datetime
from polling_agent.crew import PollingAgent


st.set_page_config(page_title="LLM Poll Generator", layout="centered")

st.title("🧠 LLM Polling Agent")
st.markdown("Generate social media posts and polls using CrewAI!")

with st.form("input_form"):
    topic = st.text_input("Enter a topic:", value="AI LLMs")
    year = st.text_input("Enter current year:", value=str(datetime.now().year))
    submitted = st.form_submit_button("Run Agent")

if submitted:
    st.info("Running the agent... this might take a few seconds.")

    # Run the crew with user input
    try:
        inputs = {
            "topic": topic,
            "current_year": year
        }

        PollingAgent().crew().kickoff(inputs=inputs)
        st.success("Agent run completed. See results below:")

        # Read and display Twitter post
        if os.path.exists("twitter_post.json"):
            with open("twitter_post.json") as f:
                twitter_data = json.load(f)
            st.subheader("🐦 Twitter Post")
            st.code(twitter_data.get("Twitter_Post", {}).get("tweet_text", "No data"), language="markdown")

        # Read and display Poll (Twitter + LinkedIn)
        if os.path.exists("poll.json"):
            with open("poll.json") as f:
                poll_data = json.load(f)

            st.subheader("📊 Twitter Poll")
            twitter_poll = poll_data.get("Twitter_Poll", {})
            st.markdown(f"**Question:** {twitter_poll.get('poll_question', '')}")
            st.markdown("**Options:**")
            for opt in twitter_poll.get("poll_options", []):
                st.markdown(f"- {opt}")
            st.code(twitter_poll.get("tweet_text", ""), language="markdown")

            st.subheader("🔗 LinkedIn Poll")
            linkedin_poll = poll_data.get("LinkedIn_Poll", {})
            st.markdown(f"**Question:** {linkedin_poll.get('poll_question', '')}")
            st.markdown("**Options:**")
            for opt in linkedin_poll.get("poll_options", []):
                st.markdown(f"- {opt}")
            st.code(linkedin_poll.get("post_text", ""), language="markdown")

        # Read and display LinkedIn post
        if os.path.exists("linkdin_post.json"):
            with open("linkdin_post.json") as f:
                linkedin_data = json.load(f)
            st.subheader("🔗 LinkedIn Post")
            st.code(linkedin_data.get("LinkedIn_Post", {}).get("post_text", "No data"), language="markdown")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

import streamlit as st
import json
import os

def load_json_safe(filepath):
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        with open(filepath) as f:
            return json.load(f)
    return {}

def display_generated_content():
    st.markdown("## 📄 Generated Output")

    # --- Twitter Post ---
    twitter_post_data = load_json_safe("twitter_post.json")
    twitter_post = twitter_post_data.get("Twitter_Post", {})
    if twitter_post:
        st.subheader("🐦 Twitter Post")
        st.code(twitter_post.get("tweet_text", "No tweet found."), language="markdown")

    # --- Poll (Twitter + LinkedIn) ---
    poll_data = load_json_safe("poll.json")
    if poll_data:
        twitter_poll = poll_data.get("Twitter_Poll", {})
        linkedin_poll = poll_data.get("LinkedIn_Poll", {})

        if twitter_poll:
            st.subheader("📊 Twitter Poll")
            st.markdown(f"**Question:** {twitter_poll.get('poll_question', '')}")
            st.markdown("**Options:**")
            for opt in twitter_poll.get("poll_options", []):
                st.markdown(f"- {opt}")
            st.code(twitter_poll.get("tweet_text", ""), language="markdown")

        if linkedin_poll:
            st.subheader("🔗 LinkedIn Poll")
            st.markdown(f"**Question:** {linkedin_poll.get('poll_question', '')}")
            st.markdown("**Options:**")
            for opt in linkedin_poll.get("poll_options", []):
                st.markdown(f"- {opt}")
            st.code(linkedin_poll.get("post_text", ""), language="markdown")

    # --- LinkedIn Post ---
    linkedin_post_data = load_json_safe("linkdin_post.json")
    linkedin_post = linkedin_post_data.get("LinkedIn_Post", {})
    if linkedin_post:
        st.subheader("🔗 LinkedIn Post")
        st.code(linkedin_post.get("post_text", "No LinkedIn post found."), language="markdown")

    # --- Fallback if no files found ---
    if not any([twitter_post, poll_data, linkedin_post]):
        st.warning("No valid output found. Run the agent first.")
    from social.twitter import post_tweet, post_poll
    from social.linkedin import post_linkedin,post_linkedin_poll

    # Buttons after display
    if twitter_post:
        if st.button("📤 Post to Twitter"):
            tweet_id = post_tweet(twitter_post["tweet_text"])
            st.success(f"Tweet posted successfully! Tweet ID: {tweet_id}")

    if poll_data.get("Twitter_Poll"):
        if st.button("📤 Post Twitter Poll"):
            tweet_id = post_poll(
                poll_data["Twitter_Poll"]["tweet_text"],
                poll_data["Twitter_Poll"]["poll_options"]
            )
            st.success(f"Poll posted successfully! Tweet ID: {tweet_id}")

    if linkedin_post:
        if st.button("📤 Post LinkedIn Article"):
            success = post_linkedin(linkedin_post["post_text"])
            if success:
                st.success("Posted to LinkedIn successfully!")
            else:
                st.error("LinkedIn post failed. Check your credentials.")

    if linkedin_poll:
        if st.button("📤 Post LinkedIn Poll"):
            success = post_linkedin_poll(
                linkedin_poll["post_text"],
                linkedin_poll["poll_question"],
                linkedin_poll["poll_options"],
                poll_duration_days=7
            )
            if success:
                st.success("LinkedIn poll posted successfully!")
            else:
                st.error("Failed to post LinkedIn poll. Check your credentials or API limits.")

display_generated_content()

