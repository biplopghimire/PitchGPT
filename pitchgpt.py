import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

class PitchGPT:
    def __init__(self, model_type='gemini_api', model_name='gemini-2.5-flash'):
        if model_type == 'gemini_api':
            from gemini_api import GeminiAPI
            load_dotenv()
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise RuntimeError("GEMINI_API_KEY not found in .env file")
            self.model = GeminiAPI(api_key=api_key, model_name=model_name)
            self.model_type = 'gemini_api'
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
        
        self.prompts = self._load_prompts('prompts.json')

    def _load_prompts(self, prompts_file):
        if os.path.exists(prompts_file):
            with open(prompts_file, 'r') as f:
                return json.load(f)
        else:
            raise FileNotFoundError(f"Prompts file '{prompts_file}' not found.")

    def analyze_pitch(self, pitch_text, prompt_key='default_analysis', custom_prompt=None):
        if custom_prompt:
            prompt = custom_prompt
        else:
            prompt_template = self.prompts.get(prompt_key, self.prompts.get('default_analysis', ''))
            prompt = prompt_template.format(pitch_text=pitch_text)
        
        if self.model:
            response = self.model.generate_content(prompt)
            return response.text
        else:
            raise RuntimeError("Model is not initialized.")