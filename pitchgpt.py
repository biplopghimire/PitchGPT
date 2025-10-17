import os
from dotenv import load_dotenv
import google.generativeai as genai

class PitchGPT:
    def __init__(self, model_name='gemini-2.5-flash'):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not found in .env file")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def analyze_pitch(self, pitch_text):
        prompt = f"""
        Analyze this startup pitch and provide:
        1. Two potential risks
        2. Three follow-up questions for due diligence

        Structure your response in clear sections with bullet points.
        Pitch: {pitch_text}
        """
        response = self.model.generate_content(prompt)
        return response.text