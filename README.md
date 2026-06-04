# 📰 Automated AI-Powered Newsletter Pipeline

> A production-grade, end-to-end pipeline that autonomously fetches, filters, deduplicates, summarises, and distributes a curated news digest - using multi-model GPT pipelines, few-shot learning, and automated email delivery.

**Built with:** Python · GPT-4o · GPT-4 · Selenium · Brevo API · Pandas · HTML

---

## 🧠 What This Project Does

Most newsletter tools either scrape broadly (producing noise) or require heavy manual curation. This pipeline solves both problems by combining web scraping with a **three-stage LLM filtering system** - ensuring only relevant, unique, high-quality articles reach subscribers.

The pipeline runs from raw Google News → filtered digest → formatted HTML email → distributed to subscriber list, with human-in-the-loop verification at the final stage.

---

## 🏗️ Pipeline Architecture

```
Google News (Selenium)
        │
        ▼
  Raw Articles DataFrame
        │
        ▼
┌─────────────────────────────────────────┐
│         3-Stage LLM Filter              │
│                                         │
│  Stage 1: Relevancy Check (GPT-4o)      │
│  → Few-shot examples mark True/False    │
│                                         │
│  Stage 2: Duplicacy Check (GPT-4)       │
│  → Overlap scored 1–10, threshold ≥ 6  │
│                                         │
│  Stage 3: Manual Review                 │
│  → Human verification before send      │
└─────────────────────────────────────────┘
        │
        ▼
  Filtered Articles
        │
        ▼
  GPT-4 Summarisation + Intro Generation
        │
        ▼
  HTML Newsletter Assembly
        │
        ▼
  Brevo Email API → Subscriber List
```

---

## ✨ Key Technical Features

| Component | What it does | Model used |
|---|---|---|
| News ingestion | Selenium scrapes Google News for top 10 articles per keyword | - |
| Relevancy filter | Few-shot learning classifies articles as relevant/irrelevant | GPT-4o |
| Duplicacy filter | Scores article overlap 1–10, filters repeats above threshold | GPT-4 |
| Summarisation | Condenses each article into digest-ready summary | GPT-4 |
| Intro generation | Auto-generates newsletter intro based on topics covered | GPT-4 |
| Email delivery | Sends HTML digest to subscriber list via Brevo transactional API | - |

### Why two different GPT models?
GPT-4o handles the **relevancy check** - it's fast and accurately follows binary classification instructions. GPT-4 handles **duplicacy scoring** - it better understands semantic overlap and nuanced similarity. Using the right model for each task reduces cost and improves accuracy.

---

## 🔍 Few-Shot Learning Implementation

The relevancy and duplicacy checks both use **few-shot prompting** - a technique where the model is shown labelled examples before being asked to classify new inputs.

```python
# Example: Relevancy check prompt structure
examples = [
    {"article": "RBI raises repo rate by 25bps...", "relevant": True},
    {"article": "Celebrity spotted at airport...", "relevant": False},
    ...
]
# New articles are classified against the topic list + examples
```

This approach was adapted from the **weekly news digest** system I built professionally - where the same few-shot pipeline reduced content noise by ~40%.

---

## 📁 Repository Structure

```
├── newsbot.py       # Full pipeline - scrape → filter → summarise → send
├── README.md
```

> The pipeline is implemented as a single orchestrated script with clearly sectioned stages, designed to run in Google Colab or locally.

---

## 🚀 Setup & Usage

### Prerequisites

```bash
pip install openai sib-api-v3-sdk selenium pandas
```

You will need:
- [OpenAI API key](https://platform.openai.com/) - GPT-4 and GPT-4o access
- [Brevo account](https://www.brevo.com/) - free tier supports up to 300 emails/day
- Chrome + ChromeDriver - for Selenium headless scraping
- A subscriber list configured in Brevo

### Configuration

Update the `queries` list in `newsbot.py` with your target topics:

```python
queries = [
    "AI machine learning 2024",
    "data science industry trends",
    # add your domain-specific keywords
]
```

Set your API keys as environment variables:

```bash
export OPENAI_API_KEY=your_key
export BREVO_API_KEY=your_key
```

### Running the Pipeline

```bash
python newsbot.py
```

The pipeline will:
1. Scrape Google News for each query
2. Run the 3-stage LLM filter automatically
3. Pause at manual review step (Stage 3) for your verification
4. Generate the HTML digest
5. Send to your Brevo subscriber list

---

## 🛠️ Tech Stack

`Python` `GPT-4o` `GPT-4` `Selenium` `ChromeDriver` `Pandas` `Brevo API` `HTML/CSS` `Google Colab`

---

## 💡 Real-World Application

This pipeline was developed based on patterns from a professional NLP automation system built for **one of the company I worked in** - where a similar LLM-driven digest workflow reduced manual content curation effort by **50–60%** and served weekly intelligence reports to leadership teams.

---

## 🔮 Potential Extensions

- Schedule with Airflow or GCP Cloud Scheduler for fully automated weekly sends
- Add a Streamlit dashboard to preview digests before send
- Extend to multi-language news sources using translation APIs
- Fine-tune a small model on your domain for faster, cheaper classification

---
