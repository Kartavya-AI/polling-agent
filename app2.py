import streamlit as st
import json
import os
from datetime import datetime
from polling_agent.crew import PollingAgent


st.set_page_config(page_title="LLM Poll Generator", layout="centered")

st.title("🧠 LLM Polling Agent")
st.markdown("Generate social media posts and polls using CrewAI!")
import streamlit as st
import os

with st.sidebar:
    st.header("⚙️ API & Model Settings")

    # --- AI Services ---
    st.subheader("🧠 AI & Search APIs")

    gemini_api_key = st.text_input(
        "Gemini API Key",
        type="password",
        value=st.session_state.get("GEMINI_API_KEY", ""),
        help="Enter your Gemini (Google AI) API key"
    )

    serper_api_key = st.text_input(
        "Serper API Key",
        type="password",
        value=st.session_state.get("SERPER_API_KEY", ""),
        help="Enter your Serper (Google Search) API key"
    )

    model_choice = st.selectbox(
        "AI Model",
        ["gemini/gemini-2.5-flash-preview-05-20", "gemini-pro", "mistral-medium"],
        index=["gemini/gemini-2.5-flash-preview-05-20", "gemini-pro", "mistral-medium"].index(
            st.session_state.get("MODEL", "gemini/gemini-2.5-flash-preview-05-20")
        ),
        help="Select the AI model to use"
    )

    # --- Twitter API ---
    st.subheader("🐦 Twitter API Keys")

    twitter_consumer_key = st.text_input(
        "Consumer Key (API Key)", type="password",
        value=st.session_state.get("TWITTER_CONSUMER_KEY", "")
    )
    twitter_consumer_secret = st.text_input(
        "Consumer Secret (API Secret)", type="password",
        value=st.session_state.get("TWITTER_CONSUMER_SECRET", "")
    )
    twitter_access_token = st.text_input(
        "Access Token", type="password",
        value=st.session_state.get("TWITTER_ACCESS_TOKEN", "")
    )
    twitter_access_token_secret = st.text_input(
        "Access Token Secret", type="password",
        value=st.session_state.get("TWITTER_ACCESS_TOKEN_SECRET", "")
    )

    # --- LinkedIn API ---
    st.subheader("🔗 LinkedIn API Keys")

    linkedin_access_token = st.text_input(
        "LinkedIn Access Token", type="password",
        value=st.session_state.get("LINKEDIN_ACCESS_TOKEN", "")
    )
    linkedin_person_urn = st.text_input(
        "LinkedIn Person URN",
        value=st.session_state.get("LINKEDIN_PERSON_URN", ""),
        help="Format: urn:li:person:xxxxxxx"
    )

    # --- Save Settings Button ---
    if st.button("💾 Save Settings"):
        updated = False

        # Store all key-value pairs in a list to loop over
        api_settings = {
            "GEMINI_API_KEY": gemini_api_key,
            "SERPER_API_KEY": serper_api_key,
            "MODEL": model_choice,
            "TWITTER_CONSUMER_KEY": twitter_consumer_key,
            "TWITTER_CONSUMER_SECRET": twitter_consumer_secret,
            "TWITTER_ACCESS_TOKEN": twitter_access_token,
            "TWITTER_ACCESS_TOKEN_SECRET": twitter_access_token_secret,
            "LINKEDIN_ACCESS_TOKEN": linkedin_access_token,
            "LINKEDIN_PERSON_URN": linkedin_person_urn
        }

        # Save to session and env
        for key, value in api_settings.items():
            if value:
                st.session_state[key] = value
                os.environ[key] = value
                updated = True

        if updated:
            st.success("✅ Settings saved successfully!")
        else:
            st.error("❌ Please enter at least one API key or model selection.")

with st.form("input_form"):
    topic = st.text_input("Enter a topic:", value="AI LLMs")
    submitted = st.form_submit_button("Run Agent")

if submitted:
    st.info("Running the agent... this might take a few seconds.")

    # Run the crew with user input
    try:
        inputs = {
            "topic": topic,
            "current_year": str(datetime.now().year)
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
    tweet_text = twitter_post_data.get("tweet_text")
    if tweet_text:
        st.subheader("🐦 Twitter Post")
        st.code(tweet_text, language="markdown")

    # --- LinkedIn Post ---
    linkedin_post_data = load_json_safe("linkdin_post.json")
    post_text = linkedin_post_data.get("post_text")
    if post_text:
        st.subheader("🔗 LinkedIn Post")
        st.code(post_text, language="markdown")
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


    # --- Fallback if nothing available ---
    if not any([tweet_text, post_text, twitter_poll, linkedin_poll]):
        st.warning("No valid output found. Run the agent first.")
        return
    from social.twitter import post_tweet, post_poll
    from social.linkedin import post_linkedin,post_linkedin_poll

    # --- Posting Buttons ---
    if tweet_text:
        if st.button("📤 Post to Twitter"):
            tweet_id = post_tweet(tweet_text)
            st.success(f"Tweet posted successfully! Tweet ID: {tweet_id}")

    if poll_data.get("Twitter_Poll"):
        if st.button("📤 Post Twitter Poll"):
            tweet_id = post_poll(
                poll_data["Twitter_Poll"]["tweet_text"],
                poll_data["Twitter_Poll"]["poll_options"]
            )
            st.success(f"Poll posted successfully! Tweet ID: {tweet_id}")

    if post_text:
        if st.button("📤 Post LinkedIn Article"):
            success = post_linkedin(post_text)
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

