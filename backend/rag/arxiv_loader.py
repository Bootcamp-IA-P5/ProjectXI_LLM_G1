import arxiv
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class ArxivLoader:
    """ Descargar papers de ArXiv"""
    
    def __init__(self, max_papers: int = 5): 
        self.max_papers=max_papers
        # ArXiv API no requiere API Key
        self.client = arxiv.Client()
        
    def search_and_download(self, query: str) -> list[Dict]:
        """
        Busca papers en ArXiv
        
        Input: "cambio climatico"
        Output: Lista de dicts con:
            -title
            -authors
            -published
            -summary
            -pdf_url
        """
        try:
            # ¿Qué hace arxiv.Search()? Busca papers ordenando los mas recientes primero
            search = arxiv.Search(
                query=query,
                max_results=self.max_papers,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending
            )
            
            papers = []
            
            # Que es este loop? Entiendo que va guardando los resultados en la lista papers, guardando los campos que nos interesan
            for result in self.client.results(search):
                paper_data = {
                    "title": result.title,
                    "authors": [author.name for author in result.authors],
                    "published": result.published.year,
                    "summary": result.summary,
                    "pdf_url": result.pdf_url,
                    "arxiv_id": result.entry_id.split('/abs/')[-1]
                }
                papers.append(paper_data) 
                logger.info(f"✅ Paper encontrado: {result.title[:50]}...")
                
            if not papers:
                logger.warning(f"⚠️ No papers encontrados para: {query}")
                return []
            
            logger.info(f"✅ {len(papers)} papers descargados exitosamente")
            return papers
        
        
        except Exception as e:        
            logger.error(f"❌ Error buscando en ArXiv: {e}") 
            return [] # Devuelve lista vacia para fallback