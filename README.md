# 📰 Automated News Digest Generator
This repository contains a Python-based pipeline to fetch, filter, summarize, and distribute a custom news digest using web scraping, OpenAI GPT models, and Brevo’s email API.

📦 2.1. Installing Dependencies
Installs required Python packages such as:

openai

sib_api_v3_sdk

selenium

pandas

datetime, etc.

These are used throughout the notebook.

🗞️ 2.2. Extracting News
Loads Selenium and configures it to run a headless Chromium browser.

Fetches news articles from Google News based on search terms provided in the queries list.

Constructs a pandas DataFrame from the scraped content.

Converts date formats using the convert_to_datetime function.

✅ You can run this section directly in Google Colab. Modify the queries list if you want different keywords.

🤖 2.3. Filtering News with OpenAI
Sets up multiple OpenAI engines for various tasks:

gpt-4o and gpt-4 are used for different news filtration logics.

generate_newsletter_content: Creates summaries for each news article.

generate_newsletter_intro: Writes an intro paragraph for the digest based on the news topics.

✅ This section can also be run as-is unless you want to tweak model versions or hyperparameters.

🧹 2.4. Filtering News
🔎 2.4.1. Relevancy Check
Uses few-shot learning with examples of relevant and irrelevant articles.

Articles are evaluated for relevancy via the gpt-4o engine.

Filters out irrelevant articles from the DataFrame.

🔁 2.4.2. Duplicacy Check
Uses few-shot learning to detect overlapping content.

Articles are rated 1–10 based on similarity (1 = full overlap, 10 = unique).

Threshold of 6: articles scoring below are marked as duplicates (True), others as unique (False).

gpt-4 engine is used here for better consistency with logical filtering.

Filters out duplicated articles from the DataFrame.

👁️ 2.4.3. Manual Check
Human verification step to review final article set.

Ensures high-quality, relevant content before generating the digest.

Manual drops or edits can be performed here if necessary.

🧾 2.5. Designing HTML for News Digest
HTML template is generated using the final filtered DataFrame.

Includes:

Styling

Hyperlinks (subscribe/unsubscribe)

Optional Google Alerts button for real-time notifications

Outputs:

Structured newsletter-ready HTML

Final HTML version for email distribution

📧 2.6. Email Distribution
Uses Brevo transactional email API.

Configures sib_api with an API key.

Sends the final HTML digest to the subscribers listed in Brevo.

✅ Summary
Step	Description
2.1	Install dependencies
2.2	Scrape news using Selenium
2.3	Use GPT models for summarization & intro
2.4	Filter for relevance, duplicacy, and quality
2.5	Generate and format HTML
2.6	Email the digest via Brevo

📌 Notes
The system requires minimal human input once set up.

Only changes typically needed are in the queries list or OpenAI engine settings.
