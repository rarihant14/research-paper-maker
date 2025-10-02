
import asyncio
from .services import tavily_search, summarize_text, generate_section, format_citations
from .Jobs import JOBS
from .utilis import track_with_langsmith

def compose_plaintext(sections, citations, topic):
    """Format research paper as clean plain text."""
    paper = f"{topic}\n\n"
    for key in ["Abstract","Introduction","Lit Review","Methodology","Results","Discussion","Conclusion"]:
        if key in sections:
            label = "Literature Review" if key == "Lit Review" else key
            paper += f"{label}:\n{sections[key].strip()}\n\n"
    paper += "References:\n"
    for i, line in enumerate(citations.splitlines(), start=1):
        paper += f"{i}. {line}\n"
    return paper.strip()

# YOOO LangSmith 
@track_with_langsmith
async def run_workflow(job_id, topic, style, words):
    """Generate research paper sections, citations, and plain-text output."""
    try:
        #Retrieve
        sources = await tavily_search(topic)

        #Summarize 
        summaries = await asyncio.gather(*(summarize_text(s["abstract"]) for s in sources))

        #sections
        sections = {}
        for sec in ["Abstract","Introduction","Lit Review","Methodology","Results","Discussion","Conclusion"]:
            sec_text = await generate_section(sec, topic, summaries, style, words // 7)
            sections[sec] = sec_text

        #  Formatting 
        citations = format_citations(sources)

        # Store job 
        JOBS[job_id]["sections"] = sections
        JOBS[job_id]["references"] = citations
        JOBS[job_id]["topic"] = topic
        JOBS[job_id]["output_plain"] = compose_plaintext(sections, citations, topic)
        JOBS[job_id]["status"] = "completed"

    except Exception as e:
        JOBS[job_id]["status"] = "failed"
        JOBS[job_id]["error"] = str(e)
