# agents/llm_config.py
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import Runnable
from typing import Any, Dict
from config import Config

def create_analyzer_chain() -> Runnable:
    llm = ChatGroq(
        api_key=Config.GROQ_API_KEY,
        model_name="mixtral-8x7b-32768",
        temperature=0.3,
        max_tokens=4096
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Tu es un expert en analyse de littérature scientifique.
        Analyse les articles fournis et produit :
        1. Un résumé synthétique
        2. Les points clés
        3. La méthodologie commune
        4. Les citations importantes
        Utilise des sections clairement délimitées."""),
        ("human", "{papers_text}")
    ])
    
    return prompt | llm | StrOutputParser()

def create_writer_chain() -> Runnable:
    llm = ChatGroq(
        api_key=Config.GROQ_API_KEY,
        model_name="llama-70b-4096",
        temperature=0.7
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Tu es un expert en rédaction scientifique.
        Génère une revue de littérature structurée basée sur l'analyse fournie."""),
        ("human", """{
            Analyse fournie:
            
            Résumé:
            {summary}
            
            Points clés:
            {key_points}
            
            Méthodologie:
            {methodology}
            
            Citations:
            {citations}
            }""")
    ])
    
    return prompt | llm | StrOutputParser()