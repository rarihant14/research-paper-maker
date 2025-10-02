# backend/services.py
import asyncio
import os
import random
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

# Fake async services
async def tavily_search(topic, top_k=5):
    """Simulate searching papers."""
    await asyncio.sleep(0.2)
    return [{"title": f"Paper {i+1}", "abstract": f"Abstract {i+1} for {topic}"} for i in range(top_k)]

async def summarize_text(text):
    """Simulate summarizing text."""
    await asyncio.sleep(0.1)
    phrases = [
        "This study highlights", 
        "Our research indicates", 
        "Findings suggest", 
        "Analysis reveals", 
        "The data confirms"
    ]
    return f"{random.choice(phrases)} {text.lower()}."

async def generate_section(section_name, topic, summaries, style, word_count):
    """Generate slightly varied content per section."""
    await asyncio.sleep(0.1)
    # Differentpatterns 
    templates = {
        "Abstract": f"The paper discusses {topic}, emphasizing key insights derived from recent studies.",
        "Introduction": f"Introducing {topic}, we explore its importance and relevance in modern contexts.",
        "Lit Review": f"Literature review shows previous work on {topic} covering various methods and approaches.",
        "Methodology": f"Our methodology examines {topic} using rigorous analysis and structured approach.",
        "Results": f"The results indicate notable trends and observations related to {topic}.",
        "Discussion": f"The discussion interprets the findings, reflecting on implications for {topic}.",
        "Conclusion": f"In conclusion, this research on {topic} provides valuable insights and future directions."
    }

    # summary 
    snippet = " ".join(random.sample(summaries, min(2, len(summaries)))) if summaries else ""
    section_text = f"{templates.get(section_name, '')} {snippet}"
    # Limi word count
    words = section_text.split()
    if len(words) > word_count:
        section_text = " ".join(words[:word_count])
    return section_text


def format_citations(sources):
    return "\n".join([f"{src['title']} — https://example.com/{i+1}" for i, src in enumerate(sources)])
