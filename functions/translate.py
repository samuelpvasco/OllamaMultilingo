import json
import messages

def detect_region(text: str) -> tuple:
    prompt = ("You are a linguistic classification API. Analyze the following text and determine its language. "
        "Your response must strictly be a valid JSON object with the keys 'name' (the language name in English) "
        "and 'code' (the 5-letter ISO code, for example 'pt-BR'). Do not include any other text, markdown blocks, or explanation.\n\n"
        f"Text to analyze: {text}")

    _, response_text = messages.send_message(
        history=[{'role': 'user', 'content': prompt}],
        model='llama3.2:1b',
        stream=False
    )

    try:
        cleaned_json = response_text.replace("```json", "").replace("```", "").strip()
        data = json.loads(cleaned_json)
        return data['name'], data['code']
    except Exception:
        return "English", "en-US"
    

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

