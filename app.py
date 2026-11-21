"""PS68 - Marketing Email Generator (Streamlit + Gemini)."""
import json
import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(override=True)
MODEL = "gemini-3.8-flash"

SYSTEM_PROMPT = """You are an expert copywriter for small shops in India.
Write promotional emails that are warm, clear and honest.
Rules:
- Use ONLY the shop name, offer and festival given by the user. Never invent
  discounts, dates, prices, addresses or phone numbers.
- Keep the body between 80 and 140 words, with a short greeting and a clear
  call to action.
- Match the requested tone.
- Return ONLY valid JSON, no markdown fences, in this exact shape:
{"variants":[{"label":"Variant A","subject":"...","body":"..."},
             {"label":"Variant B","subject":"...","body":"..."}]}
Variant A and Variant B must differ in angle (e.g. A = emotional/festive,
B = urgency/value)."""


def build_user_prompt(shop, offer, festival, tone):
    return (f"Shop name: {shop}\nOffer: {offer}\nFestival/occasion: {festival}\n"
            f"Tone: {tone}\nWrite 2 promotional email variants.")


def generate_emails(shop, offer, festival, tone):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found. Add it to your .env file.")
    client = genai.Client(api_key=api_key)
    resp = client.models.generate_content(
        model=MODEL,
        contents=build_user_prompt(shop, offer, festival, tone),
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.8,
            response_mime_type="application/json",
        ),
    )
    text = resp.text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(text)["variants"]


st.set_page_config(page_title="Marketing Email Generator", page_icon="📧")
st.title("📧 Marketing Email Generator")
st.caption("Promotional emails for festivals and offers, made for small shops.")

with st.form("email_form"):
    shop = st.text_input("Shop name", placeholder="Sharma Sweets")
    offer = st.text_input("Offer", placeholder="20% off on all gift boxes till 5 Nov")
    festival = st.text_input("Festival / occasion", placeholder="Diwali")
    tone = st.selectbox("Tone", ["Friendly", "Formal", "Festive", "Urgent", "Luxury"])
    submitted = st.form_submit_button("Generate emails")

if submitted:
    if not (shop.strip() and offer.strip() and festival.strip()):
        st.warning("Please fill in shop name, offer and festival.")
    else:
        with st.spinner("Writing your emails..."):
            try:
                st.session_state["variants"] = generate_emails(
                    shop.strip(), offer.strip(), festival.strip(), tone)
            except Exception as e:  # network, quota, bad JSON
                st.error(f"Could not generate emails: {e}")

for i, v in enumerate(st.session_state.get("variants", [])):
    st.subheader(v.get("label", f"Variant {i + 1}"))
    st.markdown(f"**Subject:** {v['subject']}")
    st.text_area("Body", v["body"], height=240, key=f"body_{i}")
    st.download_button("Download as .txt",
                       f"Subject: {v['subject']}\n\n{v['body']}",
                       file_name=f"email_variant_{i + 1}.txt", key=f"dl_{i}")
