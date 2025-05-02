# 📰 Automated News Digest Generator
This repository contains a Python-based pipeline to fetch, filter, summarize, and distribute a custom news digest using web scraping, OpenAI GPT models, and Brevo’s email API.

## 1. Installing Dependencies
1.1. This section installs necessary Python packages like openai, sib_api_v3_sdk, and others which are used throughout the notebook.

## 2. Extracting News
2.1. In this section we are loading Selenium and configuring the environment to run a headless Chromium browser.
2.2. This also includes code to create a DataFrame using pandas and fetching content using Selenium, aiming to structure the scraped data for further processing.
2.3. There are a set of key words/phrases which are passed in the list named queries. These are used to fetch the news articles from Google News. Top 10 articles are fetched from Google News according to the relevancy of the keyword/phrase.
2.4. The date column is converted to a standard form by running the function convert_to_datetime.

*This section can be run directly from the section header in Google Colab as it doesn't require any changes unless the list named queries needs to be updated.*

## 3. Filtering News with OpenAI
3.1. We set up engines using the OpenAI API.
3.1.1. The first two engines are using gpt-4o and gpt-4 respectively and are used in two different types of filtrations of news articles.
3.1.2. The third engine named generate_newsletter_content creates a short summary of the news articles which gets added into our news digest.
3.1.3. The fourth engine named generate_newsletter_intro creates the introduction section of the news digest based on the topics covered in the particular digest edition.

*This section can be run directly from the section header in Google Colab as it doesn’t require any changes unless the hyperparameters in the engines need to be changed or the models need to be updated.*

## 4. Filtering News
### 4.1. Relevancy Check
4.1.1. Here we use a few-shot learning technique and feed examples of news articles which are relevant and irrelevant. The relevant articles are marked with True and the irrelevant ones as False.
4.1.2. The news articles fetched using Selenium are then passed with a list of relevant topics and the OpenAI engine is used to evaluate these articles and mark them with either True or False. We are using the gpt-4o engine for this as it is fast and understands the instructions clearly.
4.1.3. We filter the DataFrame with rows which are marked relevant according to the engine.

### 4.2. Duplicacy Check
4.2.1. Here again we use a few-shot learning technique and feed examples of news articles which are repeating. The engine rates the overlap of an article on a scale of 1 to 10, where 1 being a full overlap and 10 representing a unique article.
4.2.2. We have kept a threshold of 6 to mark articles as either True or False. The articles having an overlap score greater than or equal to 6 are marked as False and the rest are marked as True.
4.2.3. False means the article is unique and True means the article has been repeated. We are using the gpt-4 engine for this, as it understands the logic of this activity better than gpt-4o.
4.2.4. We filter the DataFrame with rows having False in the column named IsDuplicate.

### 4.3. Manual Check
4.3.1. The last level check enables us to verify that all the articles present in the DataFrame are relevant for our news digest and can be used to fill the HTML code.
4.3.2. If there are any articles which need to be dropped, then that step can be done here. This enables us to keep the quality of the news digest high.
4.3.3. This step is necessary, as there needs to be human intervention to verify the work done by AI. We cannot leave this activity completely on AI as it can hamper the sanctity of our news digest.

## 5. Designing HTML for News Digest
5.1. The HTML code is written for the news digest. The DataFrame name needs to be passed initially to populate the HTML with the content.
5.2. The formatting of the HTML is done here along with attaching necessary hyperlinks like a subscribe button, unsubscribe button, and an option for the subscribers to use a real-time alert system made by Google (this is if the subscribers are interested in getting this type of service).
5.3. The subsequent cells contain code for generating HTML content and a final version of the HTML to be sent.

## 6. Email Distribution
6.1. As we are using Brevo’s transactional email API service, we configure the sib_api with our API key.
6.2. We pass the subscriber list created in Brevo and send out the final HTML populated with the content to our subscribers
