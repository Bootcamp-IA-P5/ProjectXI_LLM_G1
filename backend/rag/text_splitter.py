from typing import List

class TextSplitter:
    """ Dividir textos en chunks de tamaño fijo """
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        """ 
        chunk_size: tamaño máximo de cada chunk
        chunk_overlap: solapamiento entre chunks consecutivos
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split(self, text: str) -> List[str]:
        """
        Input: un abstarct de 200 palabras
        Output: Lista de chunks de ~500 palabras
        """
        
        # Dividir por palabras
        words = text.split()
        
        chunks = []
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
        
            chunk = ' '.join(words[i:i + self.chunk_size])
            if chunk.strip(): # Si no está vacio
                chunks.append(chunk)
                
        return chunks
        
    def split_papers(self, papers: list) -> List[dict]: 
        """
        Recibe lista de papers y divide cada uno

        Input: [
            {"title": "Paper 1", "summary": "Lorem ipsum...", ...},
            {"title": "Paper 2", "summary": "Dolor sit amet...", ...}
        ]
        
        Output: [
            {"title": "Paper 1", "chunk": "Lorem ipsum...", "chunk_id": 0},
            {"title": "Paper 1", "chunk": "...dolor sit...", "chunk_id": 1},
            {"title": "Paper 2", "chunk": "Dolor sit amet...", "chunk_id": 0},
        ]
        """
        split_papers = []

        for paper in papers:
            # Dividir el resumen (summary) en chunks
            chunks = self.split(paper["summary"])
            
            for idx, chunk in enumerate(chunks):
                split_papers.append({
                    "title": paper["title"],
                    "authors": paper["authors"],
                    "year": paper["published"],
                    "chunk": chunk,
                    "chunk_id": idx,
                    "arxiv_id": paper["arxiv_id"],
                })

        return split_papers




        
        
        
        
        