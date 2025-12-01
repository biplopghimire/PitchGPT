import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    _RICH = Console()
except Exception:  # rich is optional
    _RICH = None

from pitchgpt_rag.src.rag_context import retrieve_context

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
        self.training_examples = self._load_training_examples('training.json')

    def _load_prompts(self, prompts_file):
        if os.path.exists(prompts_file):
            with open(prompts_file, 'r') as f:
                return json.load(f)
        else:
            raise FileNotFoundError(f"Prompts file not found.")
    
    def _load_training_examples(self, training_file):
        if os.path.exists(training_file):
            with open(training_file, 'r') as f:
                return json.load(f)
        else:
            return {}
    
    def _build_few_shot_examples(self, prompt_key):
        """Build few-shot examples from training.json for the given analysis type."""
        if not self.training_examples:
            return ""
        
        examples_text = "\n# Examples:\n\n"
        
        for i, (company_name, data) in enumerate(self.training_examples.items(), 1):
            analysis_key = prompt_key  # 'default_analysis', 'verbose_analysis', or 'concise_analysis'
            
            if analysis_key not in data:
                continue
            
            examples_text += f"## Example {i}:\n\n"
            examples_text += f"**Pitch:**\n{data['pitch']}\n\n"
            examples_text += f"**Analysis:**\n{data[analysis_key]}\n\n"
        
        return examples_text

    def analyze_pitch(self, pitch_text, prompt_key='default_analysis', custom_prompt=None):
        context = retrieve_context(pitch_text, k=6)

        if custom_prompt:
            prompt_template = custom_prompt
        else:
            prompt_template = self.prompts.get(prompt_key, self.prompts.get('default_analysis', '{pitch_text}'))

        few_shot_examples = self._build_few_shot_examples(prompt_key)
        
        if few_shot_examples:
            enhanced_prompt = f"You are an expert venture capital analyst.\n{few_shot_examples}\n# Now analyze this new pitch:\n\n{prompt_template}"
        else:
            enhanced_prompt = prompt_template
        
        prompt = enhanced_prompt.format(pitch_text=pitch_text, context=context)

        if _RICH:
            _RICH.rule("Prompt Sent to Model")
            _RICH.print(Panel(Markdown(prompt), title="Prompt", border_style="cyan"))
            _RICH.rule("End of Prompt")
        else:
            print("=== Prompt Sent to Model ===")
            print(prompt)
            print("=== End of Prompt ===")
        if self.model:
            response = self.model.generate_content(prompt)
            return response.text
        else:
            raise RuntimeError("Model is not initialized.")