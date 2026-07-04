import os
import json
import requests 
from dotenv import load_dotenv

load_dotenv()

ollama_url = os.getenv("OLLAMA_URL")
ollama_models = os.getenv("OLLAMA_MODELS_URL")


def send_message(history: list, model: str, stream: bool) -> tuple:
    payload = {
        'model': model,
        'stream': stream,
        'messages': history
    }
    
    response = requests.post(url=ollama_url, json=payload, stream=stream)
    response.raise_for_status()
    
    if not stream:
        bot_answer = response.json()['message']['content']
        return response, bot_answer
        
    else:
        full_text_chunks = []
        
        print("\nAssistant: ", end="", flush=True)
        
        for line in response.iter_lines():
            if line:
                string_json = line.decode('utf-8')
                data = json.loads(string_json)
                
                chunk_content = data.get('message', {}).get('content', '')

                print(chunk_content, end="", flush=True)

                full_text_chunks.append(chunk_content)
        
        print()
        bot_answer = "".join(full_text_chunks)
        
        return None, bot_answer
        

def get_models() -> str:
    try:
        response = requests.get(ollama_models)
        
        if response.status_code == 200:
            models = response.json()['models']
            
            print('--- Available Models ---')
            for index, model in enumerate(models, start=1):
                    model_details = model['name'].split(':', 1)
                    model_name = model_details[0]
                
                    print(f'{index} - {model_name}')
                    
            selected_model = int(input('\n Type the model number: '))
            
            user_model = models[selected_model-1]
            print(f'\nSelected model: {user_model['name'].split(':', 1)[0]}')
            
        return user_model['name']
    except requests.exceptions.ConnectionError:
        print('\n There are no models available: Check your network connection')