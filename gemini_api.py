class GeminiAPI:
    def __init__(self, api_key, model_name='gemini-2.5-flash'):
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def generate_content(self, prompt):
        response = self.model.generate_content(prompt)
        return response