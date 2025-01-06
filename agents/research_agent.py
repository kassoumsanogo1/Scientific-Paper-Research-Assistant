# agents/research_agent.py
from langchain.agents import AgentExecutor, create_structured_chat_agent
from langchain_groq import ChatGroq
from langchain.tools import tool
from typing import List
from models import Paper, SearchQuery
import arxiv
from Bio import Entrez
import httpx
import asyncio
import config
from config import Config


class ResearchTools:
    @tool("search_arxiv")
    def search_arxiv(self, query: str, limit: int = 5) -> List[Paper]:
        """Recherche des articles sur ArXiv"""
        client = arxiv.Client()
        search = arxiv.Search(query=query, max_results=limit)
        papers = []
        
        for result in client.results(search):
            paper = Paper(
                id=result.entry_id,
                title=result.title,
                authors=[author.name for author in result.authors],
                abstract=result.summary,
                url=result.entry_id,
                source="arxiv",
                published_date=result.published,
                pdf_url=result.pdf_url
            )
            papers.append(paper)
            
        return papers

    @tool("search_pubmed")
    def search_pubmed(self, query: str, limit: int = 5) -> List[Paper]:
        """Recherche des articles sur PubMed"""
        Entrez.api_key = Config.PUBMED_API_KEY
        Entrez.email = "your@email.com"
        
        search_results = Entrez.read(
            Entrez.esearch(db="pubmed", term=query, retmax=limit)
        )
        
        papers = []
        if ids := search_results["IdList"]:
            details = Entrez.read(
                Entrez.efetch(db="pubmed", id=ids, rettype="xml")
            )
            
            for article in details["PubmedArticle"]:
                paper = self._parse_pubmed_article(article)
                papers.append(paper)
                
        return papers

    @tool("search_ieee")
    async def search_ieee(self, query: str, limit: int = 5) -> List[Paper]:
        """Recherche des articles sur IEEE"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "http://ieeexploreapi.ieee.org/api/v1/search/articles",
                params={
                    "apikey": Config.IEEE_API_KEY,
                    "format": "json",
                    "max_records": limit,
                    "querytext": query
                }
            )
            data = response.json()
            return [self._parse_ieee_article(article) for article in data.get("articles", [])]
