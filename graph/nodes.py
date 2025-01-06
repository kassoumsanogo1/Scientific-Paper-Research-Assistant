# graph/nodes.py
from langgraph.graph import MessageGraph
from typing import Dict, List
import json
from agents.llm_config import create_analyzer_chain
from agents.llm_config import create_writer_chain
from agents.research_agent import ResearchTools


def search_papers(state: Dict) -> Dict:
    """Node de recherche d'articles"""
    query = state["query"]
    tools = ResearchTools()
    
    papers = []
    papers.extend(tools.search_arxiv(query))
    papers.extend(tools.search_pubmed(query))
    papers.extend(tools.search_ieee(query))
    
    state["papers"] = papers
    return state

def analyze_papers(state: Dict) -> Dict:
    """Node d'analyse des articles"""
    papers = state["papers"]
    papers_text = "\n\n".join([
        f"Titre: {p.title}\nAuteurs: {', '.join(p.authors)}\n"
        f"Résumé: {p.abstract}" for p in papers
    ])
    
    analyzer_chain = create_analyzer_chain()
    analysis = analyzer_chain.invoke({"papers_text": papers_text})
    
    state["analysis"] = analysis
    return state

def write_review(state: Dict) -> Dict:
    """Node de rédaction"""
    analysis = state["analysis"]
    writer_chain = create_writer_chain()
    
    review = writer_chain.invoke({
        "summary": analysis.summary,
        "key_points": analysis.key_points,
        "methodology": analysis.methodology,
        "citations": analysis.citations
    })
    
    state["review"] = review
    return state