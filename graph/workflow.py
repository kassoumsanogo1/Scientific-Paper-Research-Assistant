# graph/workflow.py
from langgraph.graph import MessageGraph, END
from typing import Dict, Any
from nodes import search_papers
from nodes import analyze_papers
from nodes import write_review

def create_workflow() -> MessageGraph:
    workflow = MessageGraph()
    
    # Définition des nodes
    workflow.add_node("search", search_papers)
    workflow.add_node("analyze", analyze_papers)
    workflow.add_node("write", write_review)
    
    # Définition du flux
    workflow.add_edge("search", "analyze")
    workflow.add_edge("analyze", "write")
    workflow.add_edge("write", END)
    
    return workflow.compile()