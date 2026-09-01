import streamlit as st
from groq import Groq

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Groq AI ",
    page_icon="🐉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

/* Main background */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #111827 50%, #020617 100%);
    color: #f8fafc;
}

/* Hide Streamlit default elements */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Main content */
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 6rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827, #020617);
    border-right: 1px solid rgba(255,255,255,0.08);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label {
    color: #f8fafc !important;
}

/* App header */
.hero {
    text-align: center;
    padding: 25px 20px 30px 20px;
}

.hero-icon {
    font-size: 55px;
    margin-bottom: 5px;
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(90deg, #60a5fa, #a78bfa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

.hero-subtitle {
    color: #94a3b8;
    font-size: 15px;
    margin-top: 8px;
}

/* Welcome card */
.welcome-card {
    background: rgba(30, 41, 59, 0.65);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 30px;
    margin: 20px auto;
    max-width: 800px;
    text-align: center;
    box-shadow: 0 15px 40px rgba(0,0,0,0.25);
}

.welcome-card h2 {
    color: #f8fafc;
    margin-bottom: 10px;
}

.welcome-card p {
    color: #94a3b8;
    line-height: 1.7;
}

/* Feature cards */
.feature-container {
    display: flex;
    gap: 15px;
    justify-content: center;
    margin-top: 25px;
}

.feature {
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 15px;
    padding: 18px;
    width: 200px;
    text-align: center;
}

.feature-icon {
    font-size: 28px;
}

.feature-title {
    color: #e2e8f0;
    font-weight: 600;
    margin-top: 8px;
}

.feature-text {
    color: #94a3b8;
    font-size: 12px;
    margin-top: 5px;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: rgba(30, 41, 59, 0.55);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 12px 18px;
    margin: 12px 0;
}

/* Chat input */
[data-testid="stChatInput"] {
    border-radius: 20px;
}

[data-testid="stChatInput"] textarea {
    background: #1e293b !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 18px !important;
}

/* Buttons */
.stButton > button {
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.1);
    background: #1e293b;
    color: white;
    font-weight: 600;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #334155;
    border-color: #60a5fa;
}

/* Selectbox and sliders */
[data-baseweb="select"] > div {
    background-color: #1e293b;
    border-color: rgba(255,255,255,0.1);
}

[data-testid="stTextInput"] input {
    background: #1e293b;
    color: white;
    border-radius: 10px;
}

/* Status badge */
.status {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 20px;
    background: rgba(34,197,94,0.12);
    border: 1px solid rgba(34,197,94,0.25);
    color: #4ade80;
    font-size: 12px;
    margin-top: 10px;
}

/* Footer */
.app-footer {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    margin-top: 40px;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.markdown("## ⚙️ Settings")
    st.caption("Customize your AI assistant")

    st.divider()

    # API Key
    st.markdown("### 🔐 API Configuration")

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Enter your Groq API key."
    )
    # FIX: strip stray whitespace users often paste in accidentally
    api_key = api_key.strip() if api_key else ""

    st.caption("🔒 Your API key is only used for this session.")

    st.divider()

    # Model
    st.markdown("### 🧠 AI Model")

    model = st.selectbox(
        "Select Model",
        [
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b"
        ],
        index=0
    )

    st.divider()

    # Temperature
    st.markdown("### 🎨 Creativity")

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.05
    )

    if temperature < 0.5:
        st.caption("🎯 More focused and predictable")
    elif temperature < 1.2:
        st.caption("⚖️ Balanced responses")
    else:
        st.caption("✨ More creative responses")

    st.divider()

    # Clear button
    st.markdown("### 🗑️ Conversation")

    if st.button(
        "🧹 Clear Chat",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.markdown(
        """
        <div style="text-align:center; color:#64748b; font-size:12px;">
            <b>Groq AI Assistant</b><br>
            Powered by Groq LPU™
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# HERO HEADER
# =========================================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-icon">🐉</div>
        <h1 class="hero-title">Groq AI Assistant</h1>
        <div class="hero-subtitle">
            Fast • Intelligent • Powerful
        </div>
        <div class="status">● Online</div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# WELCOME SCREEN
# =========================================================
if len(st.session_state.messages) == 0:

    st.markdown(
        """
        <div class="welcome-card">
            <h2>👋 Welcome!</h2>
            <p>
                I'm your AI assistant powered by Groq.
                Ask questions, learn new concepts, generate ideas,
                write code, or just have a conversation.
            </p>

            <div class="feature-container">

                <div class="feature">
                    <div class="feature-icon">⚡</div>
                    <div class="feature-title">Fast</div>
                    <div class="feature-text">
                        Ultra-fast AI inference
                    </div>
                </div>

                <div class="feature">
                    <div class="feature-icon">🧠</div>
                    <div class="feature-title">Smart</div>
                    <div class="feature-text">
                        Powerful language models
                    </div>
                </div>

                <div class="feature">
                    <div class="feature-icon">💻</div>
                    <div class="feature-title">Coding</div>
                    <div class="feature-text">
                        Get help with programming
                    </div>
                </div>

            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================
for message in st.session_state.messages:

    avatar = "🧑" if message["role"] == "user" else "🐉"

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):
        st.markdown(message["content"])


# =========================================================
# CHAT INPUT
# =========================================================
user_input = st.chat_input(
    "Message Groq AI Assistant..."
)


# =========================================================
# MAIN CHAT LOGIC
# =========================================================
if user_input:

    # API key check
    if not api_key:
        st.warning(
            "🔑 Please enter your Groq API Key in the sidebar first."
        )
        st.stop()

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Display user message
    with st.chat_message(
        "user",
        avatar="🧑"
    ):
        st.markdown(user_input)

    # Create Groq client
    try:
        client = Groq(api_key=api_key)

        # Assistant response
        with st.chat_message(
            "assistant",
            avatar="🐉"
        ):

            response_placeholder = st.empty()
            full_response = ""

            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": m["role"],
                        "content": m["content"]
                    }
                    for m in st.session_state.messages
                ],
                temperature=temperature,
                stream=True
            )

            # Stream response
            for chunk in completion:

                if not chunk.choices:
                    continue

                # FIX: delta can be None on some chunks (e.g. the
                # final chunk that only carries finish_reason).
                # The original code called .content directly on it,
                # which raises AttributeError: 'NoneType' object has
                # no attribute 'content' and crashes the whole request.
                delta = chunk.choices[0].delta
                content = getattr(delta, "content", None) if delta else None

                if content:
                    full_response += content

                    response_placeholder.markdown(
                        full_response + "▌"
                    )

            # FIX: guard against an empty response (e.g. the model
            # returned nothing, or was cut off). Saving/displaying an
            # empty assistant bubble looks like a broken app.
            if not full_response.strip():
                full_response = "⚠️ The model returned an empty response. Please try again."

            # Final response
            response_placeholder.markdown(
                full_response
            )

        # Save response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": full_response
            }
        )

    except Exception as e:

        # FIX: the original code left the just-appended user message
        # in st.session_state.messages with no matching assistant
        # reply whenever the API call failed. That "orphaned" message
        # would silently get resent as context on the next turn.
        # Roll it back so history stays consistent, and let the user
        # retry cleanly.
        if (
            st.session_state.messages
            and st.session_state.messages[-1]["role"] == "user"
            and st.session_state.messages[-1]["content"] == user_input
        ):
            st.session_state.messages.pop()

        st.error(
            f"❌ Something went wrong: {str(e)}"
        )


# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
    <div class="app-footer">
        Groq AI Assistant &nbsp;•&nbsp;
        Powered by Groq LPU™ &nbsp;•&nbsp;
        Built with Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
