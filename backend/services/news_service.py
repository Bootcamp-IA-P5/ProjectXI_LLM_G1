import requests
import os

class NewsService:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2/everything"

    def get_financial_news(self, query: str, idioma_code: str = "es"):
        """
        Busca noticias financieras en el idioma específico.
        """
        # NewsAPI usa códigos ISO (es, en, fr, it) que coinciden con tu sistema
        params = {
            "q": query,
            "language": idioma_code, 
            "sortBy": "relevancy",
            "pageSize": 3, # 3 noticias de calidad son suficientes para el contexto
            "apiKey": self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            articulos = data.get("articles", [])
            if not articulos:
                return "No se encontraron noticias recientes para este tema en este idioma."

            contexto = ""
            for art in articulos:
                contexto += f"- Titre/Title: {art['title']}\n  Description: {art['description']}\n\n"
            return contexto
        except Exception as e:
            return f"Error al recuperar noticias: {str(e)}"