# PS68: Marketing Email Generator

A Streamlit app that writes promotional emails for small shops. The user enters a shop name, an offer, a festival or occasion, and a tone, and the app returns two email variants, each with a subject line and body. It uses Google's Gemini API (Google AI Studio) and does not store submitted text.

This is a writing aid. The emails are AI-generated and can contain mistakes, so read and edit them before sending, and check that the offer, dates and prices are correct.

## Requirements

* Python 3.10 or newer
* A Google AI Studio Gemini API key

## Run locally

1. Create and activate a virtual environment:

```
python -m venv venv
venv\Scripts\activate
```

In Git Bash, use `source venv/Scripts/activate` instead.

2. Install dependencies:

```
python -m pip install -r requirements.txt
```

3. Create a file named `.env` next to `app.py`, add your key on one line with no quotes, and save it. Never commit `.env`.

```
GEMINI_API_KEY=your_key_here
```

4. Start the app:

```
python -m streamlit run app.py
```

Enter the shop name, offer and festival, choose a tone, and select Generate emails. Each variant can be downloaded as a `.txt` file. The model name is set by the `MODEL` line at the top of `app.py`; change it if Google retires the model you are using.

## How it works

The app sends the form inputs to Gemini with a system prompt that tells the model to use only the shop name, offer and festival given, never invent discounts, dates, prices or contact details, keep the body to 80-140 words with a clear call to action, and return JSON with two variants. Variant A takes an emotional or festive angle and Variant B an urgency or value angle. The app parses the JSON and shows each variant with a download button.

## Manual testing and screenshots

Try at least five shops and occasions in the running app. Check that the emails use only the details entered, that the tone matches the dropdown, and that the two variants are different. For example, try a sweet shop for Diwali, a clothing store for Eid, a bookstore for Holi, a bakery for Christmas and an electronics shop for New Year. Capture screenshots of the input form and the generated variants for your submission.

## App interface

![App interface](screenshots\Input2.PNG)

## Generated emails

![Generated emails](screenshots\Output2.PNG)

