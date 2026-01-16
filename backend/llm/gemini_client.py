import google.generativeai as genai

class Client:
    
    def __init__(self, api_key, model):
        self.api_key = api_key
        self.model = model
    
    def analyze_image(self, image_path, prompt):
        genai.configure(api_key=self.api_key)
        
        #subir archivo
        file = genai.upload_file(path=image_path)
        
        #Generar respuesta
        response = genai.GenerativeModel(self.model).generate_content([prompt, file])
        
        return response.text
    
    