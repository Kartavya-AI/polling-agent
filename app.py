import streamlit as st
import json
import os
from datetime import datetime
from polling_agent.crew import PollingAgent

# Page configuration with better styling
st.set_page_config(
    page_title="LLM Poll Generator", 
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
    }
    .main-header p {
        color: #f0f0f0;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .success-box {
        background: linear-gradient(45deg, #56ab2f, #a8e6cf);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        background: linear-gradient(45deg, #f093fb, #f5576c);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .info-box {
        background: linear-gradient(45deg, #4facfe, #00f2fe);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
    .sidebar .stSelectbox > div > div {
        background: #f8f9fa;
    }
    .content-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border: 1px solid #e9ecef;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin: 0.5rem 0;
    }
    .api-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced header
st.markdown("""
<div class="main-header">
    <h1>🧠 LLM Polling Agent</h1>
    <p>Generate engaging social media posts and polls using CrewAI technology</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with improved organization
with st.sidebar:
    st.markdown("### ⚙️ Configuration Panel")
    
    # --- AI Services Section ---
    with st.expander("🧠 AI & Search APIs", expanded=True):
        st.markdown("Configure your AI model and search capabilities")
        
        gemini_api_key = st.text_input(
            "Gemini API Key",
            type="password",
            value=st.session_state.get("GEMINI_API_KEY", ""),
            help="🔑 Enter your Gemini (Google AI) API key for content generation"
        )

        serper_api_key = st.text_input(
            "Serper API Key",
            type="password",
            value=st.session_state.get("SERPER_API_KEY", ""),
            help="🔍 Enter your Serper (Google Search) API key for research"
        )

        model_choice = st.selectbox(
            "AI Model",
            ["gemini/gemini-2.5-flash-preview-05-20", "gemini-pro", "mistral-medium"],
            index=["gemini/gemini-2.5-flash-preview-05-20", "gemini-pro", "mistral-medium"].index(
                st.session_state.get("MODEL", "gemini/gemini-2.5-flash-preview-05-20")
            ),
            help="🤖 Select the AI model for content generation"
        )

    # --- Twitter API Section ---
    with st.expander("🐦 Twitter API Configuration"):
        st.markdown("Configure Twitter API for posting tweets and polls")
        
        
        col1, col2 = st.columns(2)
        with col1:
            twitter_consumer_key = st.text_input(
                "Consumer Key", 
                type="password",
                value=st.session_state.get("TWITTER_CONSUMER_KEY", ""),
                help="🔑 Twitter API Consumer Key"
            )
        with col2:
            twitter_consumer_secret = st.text_input(
                "Consumer Secret", 
                type="password",
                value=st.session_state.get("TWITTER_CONSUMER_SECRET", ""),
                help="🔒 Twitter API Consumer Secret"
            )
        
        col3, col4 = st.columns(2)
        with col3:
            twitter_access_token = st.text_input(
                "Access Token", 
                type="password",
                value=st.session_state.get("TWITTER_ACCESS_TOKEN", ""),
                help="🎫 Twitter Access Token"
            )
        with col4:
            twitter_access_token_secret = st.text_input(
                "Access Token Secret", 
                type="password",
                value=st.session_state.get("TWITTER_ACCESS_TOKEN_SECRET", ""),
                help="🔐 Twitter Access Token Secret"
            )

    # --- LinkedIn API Section ---
    with st.expander("🔗 LinkedIn API Configuration"):
        st.markdown("Configure LinkedIn API for posting articles and polls")
        
        linkedin_access_token = st.text_input(
            "LinkedIn Access Token", 
            type="password",
            value=st.session_state.get("LINKEDIN_ACCESS_TOKEN", ""),
            help="🔑 LinkedIn API Access Token"
        )
        
        linkedin_person_urn = st.text_input(
            "LinkedIn Person URN",
            value=st.session_state.get("LINKEDIN_PERSON_URN", ""),
            help="👤 Format: urn:li:person:xxxxxxx"
        )

    # Enhanced Save Settings Button
    st.markdown("---")
    if st.button("💾 Save All Settings", use_container_width=True):
        updated = False
        
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

        for key, value in api_settings.items():
            if value:
                st.session_state[key] = value
                os.environ[key] = value
                updated = True

        if updated:
            st.success("✅ Settings saved successfully!")
        else:
            st.error("❌ Please enter at least one API key or model selection.")

    # API Status indicators
    st.markdown("---")
    st.markdown("### 📊 API Status")
    
    # Check which APIs are configured
    apis_configured = []
    if gemini_api_key: apis_configured.append("Gemini")
    if serper_api_key: apis_configured.append("Serper")
    if twitter_access_token and twitter_access_token_secret and twitter_consumer_key and twitter_consumer_secret: apis_configured.append("Twitter")
    if linkedin_access_token and linkedin_person_urn: apis_configured.append("LinkedIn")
    
    if apis_configured:
        st.success(f"✅ Configured: {', '.join(apis_configured)}")
    else:
        st.warning("⚠️ No APIs configured")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🎯 Generate Content")
    
    # Enhanced input form
    with st.form("input_form"):
        st.markdown("#### Enter your topic to generate engaging social media content")
        
        topic = st.text_input(
            "Topic", 
            value="AI LLMs",
            help="💡 Enter any topic you want to create content about",
            placeholder="e.g., Artificial Intelligence, Climate Change, Technology Trends..."
        )
        
        col_submit, col_clear = st.columns([3, 1])
        with col_submit:
            submitted = st.form_submit_button("🚀 Generate Content", use_container_width=True)
        with col_clear:
            if st.form_submit_button("🗑️ Clear", use_container_width=True):
                st.rerun()

with col2:
    st.markdown("### 📈 Quick Stats")
    
    # Display some metrics
    files_exist = {
        "Twitter Post": os.path.exists("twitter_post.json"),
        "LinkedIn Post": os.path.exists("linkdin_post.json"), 
        "Polls": os.path.exists("poll.json")
    }
    
    for content_type, exists in files_exist.items():
        if exists:
            st.markdown(f"""
            <div class="metric-card">
                <strong>{content_type}</strong><br>
                ✅ Generated
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; text-align: center; margin: 0.5rem 0; border: 1px solid #dee2e6;">
                <strong>{content_type}</strong><br>
                ⏳ Pending
            </div>
            """, unsafe_allow_html=True)

# Content generation logic
if submitted:
    with st.spinner("🔄 Generating content... This may take a few moments."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            status_text.text("🔍 Researching topic...")
            progress_bar.progress(25)
            
            inputs = {
                "topic": topic,
                "current_year": str(datetime.now().year)
            }
            
            status_text.text("🤖 Generating content...")
            progress_bar.progress(50)
            
            PollingAgent().crew().kickoff(inputs=inputs)
            
            status_text.text("✅ Content generated successfully!")
            progress_bar.progress(100)
            
            st.success("🎉 Agent run completed successfully!")
            
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("💡 Please check your API keys and try again.")

# Helper functions
def load_json_safe(filepath):
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        with open(filepath) as f:
            return json.load(f)
    return {}

import streamlit as st

def display_content_card(title, content, icon="📝"):
    st.markdown(f"""
    <style>
        .content-card {{
            background-color: #333;
            color: white;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        .content-card h3 {{
            font-size: 1.5rem;
            color: white;
            display: flex;
            align-items: center;
        }}
        .content-card h3 svg {{
            margin-right: 10px;
        }}
        .content-card pre {{
            background-color: #444;
            padding: 15px;
            border-radius: 6px;
            color: #ddd;
            font-size: 1rem;
            overflow-x: auto;
        }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="content-card">
        <h3>{icon} {title}</h3>
        <div>
            <pre>{content}</pre>
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_poll_card(title, poll_data, icon="📊"):
    st.markdown(f"""
    <div class="content-card">
        <h3>{icon} {title}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"**❓ Question:** {poll_data.get('poll_question', 'N/A')}")
    st.markdown("**📋 Options:**")
    for i, opt in enumerate(poll_data.get("poll_options", []), 1):
        st.markdown(f"   {i}. {opt}")
    
    post_text = poll_data.get("tweet_text") or poll_data.get("post_text", "")
    if post_text:
        st.markdown("**📝 Post Text:**")
        st.code(post_text, language="markdown")

# Display generated content
def display_generated_content():
    st.markdown("---")
    st.markdown("## 📄 Generated Content")

    # Load all data
    twitter_post_data = load_json_safe("twitter_post.json")
    linkedin_post_data = load_json_safe("linkdin_post.json")
    poll_data = load_json_safe("poll.json")

    # Extract content
    tweet_text = twitter_post_data.get("Twitter_Post", {}).get("tweet_text") or twitter_post_data.get("tweet_text")
    post_text = linkedin_post_data.get("LinkedIn_Post", {}).get("post_text") or linkedin_post_data.get("post_text")
    twitter_poll = poll_data.get("Twitter_Poll", {})
    linkedin_poll = poll_data.get("LinkedIn_Poll", {})

    if not any([tweet_text, post_text, twitter_poll, linkedin_poll]):
        st.info("🔄 No content generated yet. Use the form above to create content!")
        return

    # Display content in tabs
    tab1, tab2, tab3 = st.tabs(["🐦 Twitter", "🔗 LinkedIn", "📊 Polls"])
    
    with tab1:
        if tweet_text:
            display_content_card("Twitter Post", tweet_text, "🐦")
            
            if st.button("📤 Post to Twitter", key="post_twitter", use_container_width=True):
                try:
                    from social.twitter import post_tweet
                    tweet_id = post_tweet(tweet_text)
                    st.success(f"✅ Tweet posted successfully! Tweet ID: {tweet_id}")
                except Exception as e:
                    st.error(f"❌ Failed to post tweet: {str(e)}")
        
        if twitter_poll:
            display_poll_card("Twitter Poll", twitter_poll, "📊")
            
            if st.button("📤 Post Twitter Poll", key="post_twitter_poll", use_container_width=True):
                try:
                    from social.twitter import post_poll
                    tweet_id = post_poll(
                        twitter_poll["tweet_text"],
                        twitter_poll["poll_options"]
                    )
                    st.success(f"✅ Poll posted successfully! Tweet ID: {tweet_id}")
                except Exception as e:
                    st.error(f"❌ Failed to post poll: {str(e)}")
    
    with tab2:
        if post_text:
            display_content_card("LinkedIn Post", post_text, "🔗")
            
            if st.button("📤 Post to LinkedIn", key="post_linkedin", use_container_width=True):
                try:
                    from social.linkedin import post_linkedin
                    success = post_linkedin(post_text)
                    if success:
                        st.success("✅ Posted to LinkedIn successfully!")
                    else:
                        st.error("❌ LinkedIn post failed. Check your credentials.")
                except Exception as e:
                    st.error(f"❌ Failed to post to LinkedIn: {str(e)}")
        
        if linkedin_poll:
            display_poll_card("LinkedIn Poll", linkedin_poll, "📊")
            
            if st.button("📤 Post LinkedIn Poll", key="post_linkedin_poll", use_container_width=True):
                try:
                    from social.linkedin import post_linkedin_poll
                    success = post_linkedin_poll(
                        linkedin_poll["post_text"],
                        linkedin_poll["poll_question"],
                        linkedin_poll["poll_options"],
                        poll_duration_days=7
                    )
                    if success:
                        st.success("✅ LinkedIn poll posted successfully!")
                    else:
                        st.error("❌ Failed to post LinkedIn poll. Check your credentials.")
                except Exception as e:
                    st.error(f"❌ Failed to post LinkedIn poll: {str(e)}")
    
    with tab3:
        if twitter_poll or linkedin_poll:
            if twitter_poll:
                display_poll_card("Twitter Poll", twitter_poll, "🐦")
            if linkedin_poll:
                display_poll_card("LinkedIn Poll", linkedin_poll, "🔗")
        else:
            st.info("📊 No polls generated yet.")

# Display the content
display_generated_content()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>🚀 Powered by CrewAI | Built with ❤️ using Streamlit</p>
    <p>Generate engaging social media content with AI-powered research and creativity</p>
</div>
""", unsafe_allow_html=True)