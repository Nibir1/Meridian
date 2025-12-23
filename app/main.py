import streamlit as st
from utils import run_meridian_pipeline

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Meridian AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PROFESSIONAL UI STYLING ---
# This CSS fixes the readability issues and adds a "Cyber/Tech" aesthetic.
st.markdown("""
<style>
    /* 1. Main Background */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }

    /* 2. Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #30363D;
    }

    /* 3. Chat Message Bubble (The Fix) */
    /* We force a dark background and explicit white text */
    div[data-testid="stChatMessage"] {
        background-color: #21262D; 
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 12px;
        color: #E6EDF3; /* Bright white-grey text */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* 4. Highlight the User vs Assistant slightly */
    div[data-testid="stChatMessage"][data-testid="user"] {
        background-color: #1E1E1E;
    }

    /* 5. Input Box Styling */
    .stTextInput > div > div > input {
        color: white;
        background-color: #0d1117;
        border: 1px solid #30363D;
    }

    /* 6. Expander Styling (Logic Trace) */
    .streamlit-expanderHeader {
        background-color: #161B22;
        color: #8B949E;
        border-radius: 8px;
    }
    
    /* 7. Header Typography */
    h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: CONTEXT CONTROLS ---
st.sidebar.title("🚀 Meridian Core")
st.sidebar.caption("Intelligent Context Orchestration")
st.sidebar.markdown("---")

st.sidebar.subheader("👤 Active Persona")

# Define our Seeded Users
personas = {
    "Sarah (CTO) - Technical": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
    "Marcus (CEO) - Strategic": "b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22"
}

selected_persona = st.sidebar.radio(
    "Select User Profile:",
    list(personas.keys()),
    index=0
)
user_id = personas[selected_persona]

st.sidebar.markdown("---")
st.sidebar.info(
    "**💡 System Logic:**\n\n"
    "1. **Identity Layer:** Injects User Profile (Bio, Role).\n"
    "2. **Intent Layer:** Routes to Tech docs vs Business docs.\n"
    "3. **RAG Layer:** Retrieves only relevant vectors."
)

# --- MAIN CHAT INTERFACE ---
st.title("Meridian Consultant")
st.markdown("#### The AI that thinks before it speaks.")

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask Meridian (e.g., 'What is the pricing?' or 'How do I authenticate?')"):
    
    # 1. Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Trigger Logic Layer
    # We use a distinct visual indicator for "Thinking"
    with st.status(f"🧠 Processing as {selected_persona.split()[0]}...", expanded=True) as status:
        st.write("🔍 Identifying User Context...")
        st.write("🔀 Routing Intent...")
        
        result = run_meridian_pipeline(
            user_query=prompt,
            user_id=user_id,
            history=st.session_state.messages
        )
        
        st.write(f"📚 Retrieved {result['intent'].upper()} Knowledge...")
        status.update(label="✅ Response Generated", state="complete", expanded=False)

    # 3. Display AI Response
    with st.chat_message("assistant"):
        st.markdown(result["response"])
        
        # Professional Logic Trace
        with st.expander("🛠️ View Orchestration Logs"):
            st.markdown(f"**Intent Detected:** `{result['intent'].upper()}`")
            st.markdown("**System Prompt Injected:**")
            st.code(result['context_used'], language="text")

    st.session_state.messages.append({"role": "assistant", "content": result["response"]})