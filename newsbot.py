# Installing Dependencies
"""

!pip install --upgrade pip

!pip install openai -q

!pip install sib_api_v3_sdk -q

!pip install selenium -q

!apt-get update

!apt install -yq chromium-browser

!apt-get install -yq chromium-chromedriver

!cp /usr/lib/chromium-browser/chromedriver /usr/bin

import requests
import json
from datetime import datetime, timedelta
from prettytable import PrettyTable
import openai
from openai import OpenAI
from openai import AsyncOpenAI
from bs4 import BeautifulSoup
import pandas as pd
from __future__ import print_function
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import sys
sys.path.insert(0, '/usr/lib/chromium-browser/chromedriver')

"""---


# Extracting News

Fetching news using Selenium
"""

#!pip install selenium

#!apt-get update
#!apt install -yq chromium-browser


#!apt-get install -yq chromium-chromedriver
#!cp /usr/lib/chromium-browser/chromedriver /usr/bin

#import sys
#sys.path.insert(0, '/usr/lib/chromium-browser/chromedriver')

#from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')


chrome_options.binary_location = "/usr/bin/chromium-browser"


#driver = webdriver.Chrome('chromedriver', options=chrome_options)
driver = webdriver.Chrome(options=chrome_options)

"""Creating a dataframe

**RUN THIS**
"""

#import pandas as pd
#from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.common.exceptions import NoSuchElementException, TimeoutException

#chrome_options = # ... your chrome options here ...
driver = webdriver.Chrome(options=chrome_options)

# List of queries
queries = ['Quality Control Order', 'market surveillance India', 'Conformity assessment', 'India trade', 'Consultation paper India', 'Ministry of commerce india', 'ESG reporting', 'anti-dumping system']

all_articles = []

for query in queries:
    # Convert the query into a format suitable for URL (replace spaces with '+')
    formatted_query = query.replace(' ', '+')

    base_url = f'https://www.google.com/search?q={formatted_query}&sca_esv=80879160ea65325f&rlz=1C1ONGR_enIN1078IN1078&tbs=qdr:w&tbm=nws&sxsrf=ADLYWIK0t8aGCCuSvpwf5Hd2dNeD2SK2Sw:1716367716089&tbas=0&source=lnt&sa=X&ved=2ahUKEwjrqZWA8KCGAxUI7jgGHdq6BNQQpwV6BAgBEBM&biw=1536&bih=730&dpr=1.25'

    for page in range(1):  # Loop through 5 pages
        url = f'{base_url}&start={page * 10}'
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div#rso > div > div > div > div'))
            )
        except TimeoutException:
            print("Timed out waiting for page to load")
            continue

        news_results = driver.find_elements(By.CSS_SELECTOR, 'div#rso > div > div > div > div')

        for news_div in news_results:
            try:
                news_link = news_div.find_element(By.TAG_NAME, 'a').get_attribute('href')
                image_element = news_div.find_element(By.CSS_SELECTOR, 'img')
                image_url = image_element.get_attribute('src') if image_element else None

                divs_inside_news = news_div.find_elements(By.CSS_SELECTOR, 'a>div>div>div')

                if len(divs_inside_news) >= 4:
                    article_data = {
                        'Query': query,
                        'Link': news_link,
                        'Domain': divs_inside_news[1].text,
                        'Title': divs_inside_news[2].text,
                        'Image URL': image_url,
                        'Description': divs_inside_news[3].text,
                        'Date': divs_inside_news[4].text if len(divs_inside_news) > 4 else None
                    }
                    all_articles.append(article_data)
            except Exception as e:
                print(f"Error processing element: {e}")

driver.quit()

# Convert all articles to a DataFrame
df_all_articles = pd.DataFrame(all_articles)

def convert_to_datetime(date_str):
    if date_str is None:
        return None  # or return 'Unknown', depending on how you want to handle None values
    now = datetime.now()
    if 'days ago' in date_str:
        days = int(date_str.split(' ')[0])
        return (now - timedelta(days=days)).strftime('%Y-%m-%d')
    elif 'day ago' in date_str:
        return (now - timedelta(days=1)).strftime('%Y-%m-%d')
    elif 'hours ago' in date_str:
        hours = int(date_str.split(' ')[0])
        return (now - timedelta(hours=hours)).strftime('%Y-%m-%d %H:%M:%S')
    elif 'hour ago' in date_str:
        return (now - timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
    elif 'minutes ago' in date_str:
        minutes = int(date_str.split(' ')[0])
        return (now - timedelta(minutes=minutes)).strftime('%Y-%m-%d %H:%M:%S')
    elif 'minute ago' in date_str:
        return (now - timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S')
    elif 'seconds ago' in date_str:
        seconds = int(date_str.split(' ')[0])
        return (now - timedelta(seconds=seconds)).strftime('%Y-%m-%d %H:%M:%S')
    elif 'second ago' in date_str:
        return (now - timedelta(seconds=1)).strftime('%Y-%m-%d %H:%M:%S')
    else:
        return date_str

df_all_articles['Date Formatted'] = df_all_articles['Date'].apply(convert_to_datetime)
df_all_articles

"""---


#Setting up OPEN AI engines

Setting up OpenAI engine
"""

#### OpenAI Engine
def openai_request(instructions, task, sample = [], model_engine='gpt-4o'):
    prompt = [{"role": "system", "content": instructions },
              {"role": "user", "content": task }]
    prompt = sample + prompt
    client = OpenAI(api_key= 'sk-')
    response = client.chat.completions.create(model=model_engine, messages=prompt, temperature=0.5, max_tokens=500)
    return response.choices[0].message.content

#### OpenAI Engine for duplicacy
def openai_request_dupli(instructions, task, sample = [], model_engine='gpt-4'):
    prompt = [{"role": "system", "content": instructions },
              {"role": "user", "content": task }]
    prompt = sample + prompt
    client = OpenAI(api_key= 'sk-')
    response = client.chat.completions.create(model=model_engine, messages=prompt, temperature=0.3, max_tokens=500)
    return response.choices[0].message.content

"""Function to generate news article summary (description in the html)"""

#### Function to generate newsletter summary (description in the html)
def generate_newsletter_content(news_title, news_description):
    instructions = 'Generate a detailed summary of the following news article based on the news title and description for a newsletter with a maximum length of 300 characters. Ensure it does not miss out on the important information.'
    task = f'Title: {news_title}. Description: {news_description}.'
    client = openai.OpenAI(api_key="sk-")  # Replace with your actual API key
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"{instructions}\n{task}",
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].text

"""Function to generate summary of the news digest for intro section"""

#### Function to generate news digest summary intro (description in the html)
def generate_newsletter_intro(query_title):
    instructions = 'Generate an introduction which gives a states the topics(query_title) covered in the news digest. It should always start with "This weeks news digest". Make sure the short introduction you generate is logical and grammatically correct.'
    task = f'Title: {query_title}.'
    client = openai.OpenAI(api_key="sk-")  # Replace with your actual API key
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"{instructions}\n{task}",
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].text

"""# Filtering news

**Relevance check**
"""

def select_relevant_news_df2(news_articles, topics, n):
    instructions = f'Your task is to examine a list of News and return a list of boolean values that indicate which of the News are in scope of a list of topics. \
    Return a list of True or False values that indicate the relevance of the News. Make sure you match the total number of news passed. Always remember to close the list with square bracket.'

    task =  f"{news_articles} /n {topics}?"

    sample = [
        {"role": "user", "content": f"[Government announces new accreditation standards, Notification on upcoming accreditation seminars, India needs to enhance quality workforce and investment in R & D to achieve goal of developed nation status, New study reveals impact of accreditations on industry, DGFT to discuss trade regime of dual use goods software and technology] /n {topics}?"},
        {"role": "assistant", "content": "[True, True, True, True, True]"},
        {"role": "user", "content": f"[Accreditation-related workshop organized by private organization, Government notification on quality standards in healthcare sector, Large scale clean energy adoption critical to transforming health and air quality, Celebrity endorsements for an apparel brand, Latest movie releases] /n {topics}?"},
        {"role": "assistant", "content": "[True, True, True, False, False]"},
        {"role": "user", "content": f"[Surging Demand in the Healthcare Accreditation Evaluation Services Market, Goyal praises FCI for moderating prices of wheat and rice, Governmental policies boosting accreditation, Annual report on sports, Technology gadgets review] /n {topics}?"},
        {"role": "assistant", "content": "[True, True, True, False, False]"},
        {"role": "user", "content": f"[RBI proposes stricter rules for housing finance firms, Govt rolls out mandatory quality norms for electrical accessories, India Inc CEO Survey : One - third believe in resilience of Indian economy, Season  longest Fog  Blankets Up At 3 . 3 degrees Delhi records season coldest morning, Travel destination guide] /n {topics}?"},
        {"role": "assistant", "content": "[True, True, True, False, False]"},
        {"role": "user", "content": f"[Firewall Audit Tool Market to Get a New Boost, Higher edu institutions to be categorised as accredited or not accredited grading system to go,SEBI Proposes Framework to Address FPI Registration Expiry Challenges, Global Helideck Monitoring System Market Size To Worth USD 257.3 Million By 2033, Mandatory Activation of Audit Trail for Companies Starting FY 01.04.2023] /n {topics}?"},
        {"role": "assistant", "content": "[False, True, True, False, False]"},
        {"role": "user", "content": f"[The hottest new job in sustainability ESG controller, India Customs and Global Trade Challenges, Operon Strategist Brings Expertise in Medical Device Regulation to Medical Fair India 2024, Top kitchen innovations of 2024 revealed, Self Versus Third-party Perceptions of Female Age Health and Attractiveness Plus the Role of Facial Skin Features] /n {topics}?"},
        {"role": "assistant", "content": "[False, True, True, False, False]"},
        {"role": "user", "content": f"[The 36 best Indian original series on Netflix and Amazon Prime Video, Maintenance Quality Control Assurance Testing and Inspection Services in Connection with Roadway Repair Citywide, Sabyasachi Launches High Jewelry Collection At Bergdorf Goodman, India rushes officials to countries that are drinking less Indian tea, Ethiopian Airlines adds to Boeing backlog with 777-9 order] /n {topics}?"},
        {"role": "assistant", "content": "[False, False, False, False, False]"},
        {"role": "user", "content": f"[Tether to Start Monitoring Secondary Market for USDT, Home Surveillance Market to See Stunning Growth, Watch Bloomberg Surveillance, No such thing as bad publicity The FCA is putting that to the test, AMCs see Rs 1400 crore hit from proposal for uniform investor fee] /n {topics}?"},
        {"role": "assistant", "content": "[False, False, False, False, False]"},
        {"role": "user", "content": f"[JPMorgan Says India Index Inclusion on Track Most Clients Ready, No more unknown calls! Caller’s name to be visible on your phone, Press Information Bureau, The Digitization of ESG Reporting, Launches Annual ESG Report] /n {topics}?"},
        {"role": "assistant", "content": "[False, False, True, True, False]"}
        ]

    return instructions, task, sample

# Example usage
relevant_topics = "[Quality Control Order, market surveillance India, Conformity assessment, India trade, made in India, Consultation paper India, Ministry of commerce india, ESG reporting, product recall India, anti-dumping system]"

instructions, task, sample = select_relevant_news_df2(list(df_all_articles['Title']), relevant_topics, len(list(df_all_articles['Title'])))
relevance = openai_request(instructions, task, sample)
relevance_list = eval(relevance)
print("Number of news articles:", len(list(df_all_articles['Title'])))
print("Number of boolean checks done:", len(relevance_list))

#Ensure the lengths match by truncating or padding relevance_list
relevance_list = relevance_list[:len(list(df_all_articles['Title']))] + [False] * (len(list(df_all_articles['Title'])) - len(relevance_list))
print("Length of relevance_list:", len(relevance_list))
print("Length of df:", len(list(df_all_articles['Title'])))

df_all_articles = df_all_articles[relevance_list]
print(len(df_all_articles))
df_all_articles

"""Duplicate check

New Try (attaching overlap scores)
"""

#### Define OpenAI Prompt for news Relevance
def check_previous_posts_prompt(title, old_posts):
    instructions = f'Your objective is to compare a news title with a list of previous news and determine whether it covers a similar topic that was already covered by a previous title. \
        Rate the overlap on a scale between 1 and 10 with 1 being a full overlap and 10 representing an unrelated topic. "'
    task =  f"'{title}.' Previous News: {old_posts}."
    sample = [
        {"role": "user", "content": "'Modi announces 2024 election campaign.' Previous News: [2024 election campaign announced by Modi, Modi's popularity ratings hit all-time high, Rahul Gandhi's popularity ratings plummet, Congress party in disarray]."},
        {"role": "assistant", "content": "1"},
        {"role": "user", "content": "'Opposition announces INDIA(an opposition unity) for 2024 election campaign.' Previous News: [2024 election campaign announced by Opposition, Modi's popularity ratings hit all-time high, Rahul Gandhi's popularity ratings plummet, Congress party in disarray]."},
        {"role": "assistant", "content": "2"},
        {"role": "user", "content": "'TMC win Bengal municipal elections with landslide victory.' Previous News: [Mamta Banerjee's popularity ratings surge, TMC party in good shape, BJP party in trouble]."},
        {"role": "assistant", "content": "5"},
        {"role": "user", "content": "'Kejriwal launches new anti-corruption campaign.' Previous News: [Kejriwal's popularity ratings surge, AAP party in good shape, BJP party in trouble]."},
        {"role": "assistant", "content": "9"},
        {"role": "user", "content": "'Yogi Adityanath unveils new economic plan.' Previous News : [Yogi Adityanath's popularity ratings rise, BJP party in good shape, Congress party in trouble]."},
        {"role": "assistant", "content": "7"},
        {"role": "user", "content": "'Trai suggests new audience measurement system as part of broadcasting policy.' Previous News : [TRAI To Issue Consultation Paper For New Broadcasting Bill Soon: Chairperson]."},
        {"role": "assistant", "content": "6"},
        {"role": "user", "content": "'Foxconn end joint venture with Vedanta for semiconductor plant .' Previous News : [Modi's popularity ratings decline, BJP party in trouble, Congress party in good shape]."},
        {"role": "assistant", "content": "10"}]
    return instructions, task, sample

def previous_post_check(title, old_posts):
    # Return a high score if no previous posts to compare against, indicating uniqueness
    if not old_posts:
        return 10
    instructions, task, sample = check_previous_posts_prompt(title, old_posts)
    response = openai_request_dupli(instructions, task, sample)
    overlap_score = eval(response)
    return overlap_score

#Relevant Articles
#df_all_articles = df_all_articles[relevance_list]

# Initialize an empty list to keep track of unique titles
old_posts = []
# Initialize a list to hold both the duplicate status and the overlap scores
duplicate_info = []

# Iterate over each article in the dataframe
for index, row in df_all_articles.iterrows():
    title = row['Title']
    is_duplicate = title in old_posts

    if not is_duplicate:
        overlap_score = previous_post_check(title, old_posts)
        is_duplicate = overlap_score <= 6

    # Append a tuple or dictionary with both pieces of information
    duplicate_info.append({'IsDuplicate': is_duplicate, 'OverlapScore': overlap_score})

    if not is_duplicate:
        old_posts.append(title)

# Convert the list of dictionaries to a DataFrame
df_overlap_info = pd.DataFrame(duplicate_info)

# Concatenate the new DataFrame with the existing df_all_articles along the axis=1 (column-wise)
df_all_articles = pd.concat([df_all_articles.reset_index(drop=True), df_overlap_info.reset_index(drop=True)], axis=1)

df_all_articles

df_unique_articles = df_all_articles[df_all_articles['IsDuplicate'] == False]
print(len(df_unique_articles))
df_unique_articles

"""Manual check"""

# Manual Check and drop irrelevant articles
rows_to_drop = [24]
df_unique_articles.drop(rows_to_drop, inplace=True)
df_unique_articles

len(df_unique_articles)

"""Trying to randomise article selection"""

# First, sort df_unique_articles by 'OverlapScore' in descending order
df_unique_articles_sorted = df_unique_articles.sort_values(by='OverlapScore', ascending=False)

# Sample one article per 'Query' from the sorted DataFrame
one_per_query = df_unique_articles_sorted.groupby('Query').apply(lambda x: x.sample(n=1, random_state=42)).reset_index(drop=True)

# Get indices of selected articles
selected_indices = one_per_query.index

# Determine how many more articles we need
additional_needed = 15 - len(one_per_query)

# Exclude already selected articles from the pool for additional sampling, using the sorted DataFrame
remaining_articles = df_unique_articles_sorted[~df_unique_articles_sorted.index.isin(selected_indices)]

# If additional articles needed and remaining are not enough, allow duplicates from high score articles from remaining queries
if additional_needed > 0:
    if not remaining_articles.empty and len(remaining_articles) < additional_needed:
        # Allow selection from all articles if not enough unique articles are available
        remaining_articles = df_unique_articles_sorted[~df_unique_articles_sorted['Title'].isin(one_per_query['Title'])]
    # Sample additional articles
    additional_articles = remaining_articles.sample(n=min(additional_needed, len(remaining_articles)), replace=False, random_state=42)
else:
    additional_articles = pd.DataFrame([])

# Combine selected articles
final_selection = pd.concat([one_per_query, additional_articles]).reset_index(drop=True)

# If still not enough articles after all that, allow for more duplicates from high 'OverlapScore' articles
if len(final_selection) < 15:
    needed = 15 - len(final_selection)
    extra_articles = df_unique_articles_sorted[~df_unique_articles_sorted['Title'].isin(final_selection['Title'])]
    additional_extra_articles = extra_articles.sample(n=min(needed, len(extra_articles)), replace=False, random_state=42)
    final_selection = pd.concat([final_selection, additional_extra_articles])

# Drop any duplicates based on 'Title' to ensure uniqueness, in case of any edge cases
final_selection = final_selection.drop_duplicates(subset=['Title'], keep='first').reset_index(drop=True)

# Ensure final count is sufficient
final_selection = final_selection.head(15)

# Ensure no repetition in the final selection
assert final_selection['Title'].is_unique

# Copy final selection to a new DataFrame for use
new_selection = final_selection.copy()

# Show the final selection DataFrame
new_selection

"""**Only use below code, when you want to drop an article from the above DF**"""

row_drop= [5]
new_selection.drop(row_drop, inplace=True)
new_selection

"""---


# Designing the HTML

**RUN THIS**
"""

CURRENT_DATE = datetime.now().strftime("%B %d, %Y")
summary_intro = generate_newsletter_intro(list(df_unique_articles['Query']))

html_content_og = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>News Bulletin</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Anek+Devanagari:wdth,wght@88,300&display=swap" rel="stylesheet">
    <style>
        .anek-devanagari-title {
            font-family: "Anek Devanagari", sans-serif;
            font-optical-sizing: auto;
            font-weight: 300;
            font-style: normal;
            font-variation-settings: "wdth" 88;
        }
        body {
            font-family: 'Arial', sans-serif;
            background-color: #E8EFF1;
            margin: 0;
            padding: 0;
            color: #333;
        }
        .container {
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            color:
        }
        h1 {
            text-align: center;
            color: #4A90E2;
            font-family: 'Anek Devanagari', sans-serif;
            font-size: 60px;
            padding: 0px;
        }
        ul {
            border: 1px solid #ccc;
            border-radius: 5px;
            margin-bottom: 20px;
            padding: 0;
            background-color: #fff;
        }
        li {
            border: 1px solid #ccc;
            border-radius: 5px;
            margin-bottom: 20px;
            padding: 0px;
            background-color: #fff;
        }
        h2, h3 {
            color: #11A3D4;
        }
        p, .query {
            margin: 5px 0;
        }
        strong {
            color: #27AE60;
        }
        a {
            color: #3498DB;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .footer {
            text-align: center;
            padding: 20px;
            font-size: 0.8em;
            background-color: #2C3E50;
            color: #fff;
        }
        .footer a {
            color: #11A3D4;
        }
        .footer a:hover {
            text-decoration: underline;
            color: #CCCCCC; a lighter shade */
        }
        .query {
            font-style: italic;
        }
        .center {
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 50%;
        }
    </style>
</head>
<body>
    <div class="container">
        <img alt style="margin:0 auto 0 auto;width:100%;" class="center" img src="https://" alt="News Bulletin">
        <p style="text-align:right;">""" + CURRENT_DATE + """</p>
        <hr>
        <p style="text-align:center;">Welcome to News Bulletin, your weekly source for essential insights and trends, curated to keep you informed and ahead.</p>
        <p style="text-align:center;">""" + summary_intro + """</p>
        <hr>
        <p align="center"><a href="https://">Click here to subscribe</a></p>
    </div>
</body>
</html>
"""

"""Populating relevant news to HTML Page

new try

**RUN THIS**
"""

article_count = 0
for _, article in df_unique_articles.iterrows():
    summary = generate_newsletter_content(article['Title'], article['Description'])
    html_content_og += f"""
        <ul>
            <h3><a href='{article['Link']}'>{article['Title']}</a></h3>
            <p><strong>Source:</strong> {article['Domain']}</p>
            <p><strong>Published On:</strong> {article['Date Formatted']}</p>
            <p><strong>Summary:</strong> {summary}</p>
            <p class="query">#{article['Query']}</p>
            <br>
        </ul>
    """
    article_count += 1
    if article_count >= 16:  # Assuming you want to limit the number of articles
        break

# Adding a sentence with a hyperlink after the news articles
html_content_og += """
    <div class="container">
        <p align="center">If you would like to get real time updates for a certain topic in your email, you can setup a <a href="https://www.google.co.in/alerts">Google alerts</a> system.</p>
    </div>
"""

# Close the list and HTML content
html_content_og += """
     <div class="footer">
        If you have any comments or feedback, kindly fill this <a href="https://">google form</a>.<br><br>
        Thanks for reading.<br>
        Regards,<br>
        Manas<br><br>
        <a href="https://">Unsubscribe</a>
    </div>
</body>
</html>
"""

"""Writing HTML content to a file"""

output_file_path = "Newsletter.html"
with open(output_file_path, "w", encoding="utf-8") as file:
    file.write(html_content_og)
file.close()

print("HTML file generated successfully.")

"""# Brevo (Email Distribution)

"""

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = ''
api_client = sib_api_v3_sdk.ApiClient(configuration)

# Initialize the Contacts API and get contacts from a list
contacts_api = sib_api_v3_sdk.ContactsApi(api_client)
list_id = 3

try:
    # Get contacts from the list
    api_response = contacts_api.get_contacts_from_list(list_id)
    contacts_list = api_response.contacts
    emails_list = [{"email": contact['email']} for contact in contacts_list]  # Adjusted for object attribute access
except ApiException as e:
    print(f"Exception when calling ContactsApi->get_contacts_from_list: {e}\n")

# Prepare email content and recipients
subject = "Weekly Gunvatta Bulletin"
sender = {"name":"Team xyz","email":"xyz.@gmail.com"}
replyTo = {"name":"Team xyz","email":"xyz.@gmail.com"}
html_content = html_content_og
to = emails_list

# Initialize the Transactional Emails API and send an email
emails_api = sib_api_v3_sdk.TransactionalEmailsApi(api_client)
send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, sender=sender, subject=subject, html_content=html_content, reply_to=replyTo)

try:
    api_response = emails_api.send_transac_email(send_smtp_email)
    pprint(api_response)
except ApiException as e:
    print(f"Exception when calling SMTPApi->send_transac_email: {e}\n")

"""# Check email list (*No need to run*)"""

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = 'xkeysib-'
api_instance_list = sib_api_v3_sdk.ContactsApi(sib_api_v3_sdk.ApiClient(configuration))
list_id = 3

try:
    # Get contacts in a list
    api_response = api_instance_list.get_contacts_from_list(list_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ContactsApi->get_contacts_from_list: %s\n" % e)

contacts_list = api_response.contacts
emails_list = [{"email": contact['email']} for contact in contacts_list]
emails_list