import streamlit as st
from google import genai
from google.genai import types

# 1. Page Configuration
st.set_page_config(page_title="AI Shopping Assistant", page_icon="🛍️")
st.title("🛍️ AI Shopping Assistant")
st.caption("Showcase: Reducing product discovery time by 40% with adaptive flows.")

# 2. Initialize Gemini Client (Requires GEMINI_API_KEY in secrets)
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 3. System Instructions
sys_instruct = """
You are an expert Shopping Assistant. Your goal is to reduce product discovery time and ensure a seamless purchase journey.
Rules:
1. Never list more than 3 products at a time.
2. Ask exactly ONE clarifying question if the request is broad.
3. Briefly explain why a product matches their input.
4. End with a clear Call to Action (e.g., "Would you like to add this to your cart?").

Catalog:
- CloudStep Running Shoes ($120) - athletic, breathable
- AeroTech Windbreaker ($85) - outdoor, water-resistant
- Urban Commuter Backpack ($95) - laptop, waterproof
"""

# 4. Manage Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        types.Content(role="user", parts=[types.Part.from_text(text="System setup: You are ready. Say hello!")]),
        types.Content(role="model", parts=[types.Part.from_text(text="Hello! What are you shopping for today?")])
    ]

# Display previous messages
for msg in st.session_state.chat_history[1:]:
    with st.chat_message(msg.role):
        st.markdown(msg.parts[0].text)

# 5. Handle User Input
if prompt := st.chat_input("What are you looking for?"):
    st.chat_message("user").markdown(prompt)
    
    st.session_state.chat_history.append(
        types.Content(role="user", parts=[types.Part.from_text(text=prompt)])
    )
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=st.session_state.chat_history,
        config=types.GenerateContentConfig(
            system_instruction=sys_instruct,
            temperature=0.2,
        )
    )
    
    with st.chat_message("model"):
        st.markdown(response.text)
        
    st.session_state.chat_history.append(
        types.Content(role="model", parts=[types.Part.from_text(text=response.text)])
    )
