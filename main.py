# main.py
from typing import Dict, Any
import asyncio
from model.models import SearchQuery
import logging
from graph.workflow import create_workflow
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ARAS")

class ARAS:
    def __init__(self):
        self.workflow = create_workflow()
        logger.info("ARAS initialisé avec LangGraph")
    
    async def process_query(self, search_query: SearchQuery) -> Dict[str, Any]:
        try:
            # État initial
            initial_state = {
                "query": search_query.query,
                "filters": search_query.filters,
                "limit_per_source": search_query.limit_per_source
            }
            
            # Exécution du workflow
            result = await self.workflow.ainvoke(initial_state)
            
            return {
                "status": "success",
                "papers": [paper.dict() for paper in result["papers"]],
                "analysis": result["analysis"],
                "review": result["review"]
            }
            
        except Exception as e:
            logger.error(f"Erreur: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": str(e)
            }

async def main():
    aras = ARAS()
    query = SearchQuery(
        query="transformer architecture deep learning",
        filters={"year": "2023-2024"},
        limit_per_source=3
    )
    
    result = await aras.process_query(query)
    print("\n=== Résultat ===")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())