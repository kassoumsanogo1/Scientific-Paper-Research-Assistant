# models.py
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class Paper(BaseModel):
    id: str
    title: str
    authors: List[str]
    abstract: str
    url: str
    source: str
    published_date: datetime
    pdf_url: Optional[str] = None
    doi: Optional[str] = None

class SearchQuery(BaseModel):
    query: str
    filters: Dict = Field(default_factory=dict)
    limit_per_source: int = 5

class AnalysisResult(BaseModel):
    summary: str
    key_points: List[str]
    methodology: Optional[str]
    citations: List[str]
    metadata: Dict