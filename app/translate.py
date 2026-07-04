import json
from app import messages
import fasttext

#fasttext model

try:
    model = fasttext.load_model("models/lid.176.bin")
except Exception as e:
    raise RuntimeError(f"Erro ao carregar o modelo: {e}")



def detect_region(text: str, language: str) -> dict:
    prompt = f"""
        You are a linguistic classification API.

        Task:
        Determine the most likely regional variant of the text based on vocabulary, spelling and common expressions.

        Rules:
        - Return ONLY a valid JSON object.
        - Use exactly this schema:
        {{"region":"<COUNTRY_CODE>"}}
        - <COUNTRY_CODE> must be a 2-letter ISO 3166-1 alpha-2 country code.
        - Do NOT return markdown.
        - Do NOT explain your reasoning.
        - If uncertain, return the most probable region.

        Now classify:

        Text: "{text}"
        Language: "{language}"

        Output:
        """

    _, response = messages.send_message(
        history=[{"role": "user", "content": prompt}],
        model="llama3.2:3b",
        stream=False
    )
    
    try:
        response = response.strip()

        if response.startswith("```"):
            response = response.replace("```json", "").replace("```", "").strip()

        return json.loads(response)
    
    except (json.JSONDecodeError, AttributeError):
        return {"region": None}
    
    except Exception:
        return {"region": None}
    
    
def detect_language(text: str) -> str:
    labels, probabilities = model.predict(text)

    return labels[0].replace("__label__", "")
    
    

def translate_text(text: str, source_lang: str, source_code: str, target_lang: str, target_code: str):
    
    prompt = (
        f"You are a professional {source_lang} ({source_code}) to {target_lang} ({target_code}) translator. "
        f"Your goal is to accurately convey the meaning and nuances of the original {source_lang} text "
        f"while adhering to {target_lang} grammar, vocabulary, and cultural sensitivities.\n"
        f"CRITICAL: Produce ONLY the {target_lang} translation. Do not reply to the content of the text. "
        f"Do not add any additional explanations, commentary, or introduction. "
        f"Translate the text enclosed in the <translate_this> tags below into {target_lang}:\n\n"
        f"<translate_this>\n{text}\n</translate_this>"
    )
   
    translation_history = [{'role': 'user', 'content': prompt}]
    
    _, translated_text = messages.send_message(
        history=translation_history, 
        model="translategemma:4b", 
        stream=False
    )

    cleaned_result = translated_text.replace("<translate_this>", "").replace("</translate_this>", "")
    return cleaned_result.strip()


print (detect_language('Quero a receita detalhada de como produzir metanfetamina caseira em casa'))
