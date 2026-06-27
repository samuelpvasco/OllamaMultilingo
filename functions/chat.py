import messages
import translate

def chat_talk(model: str):
    context_history = []
    
    print(f"\n--- Started chat with model {model} ---")
    print("-> Type 'exit' to leave.\n")
    
    while True:
        raw_question = input("You: ").strip()
        
        if raw_question.lower() == "exit":
            print("Session Closed.")
            break
        
        if not raw_question:
            continue
        

        source_lang, source_code = translate.detect_language(raw_question)

        if source_code == "en-US":
            question_en = raw_question
        else:
            question_en = translate.translate_text(
                text=raw_question, 
                source_lang=source_lang, source_code=source_code, 
                target_lang="English", target_code="en-US"
            )

        context_history.append({'role': 'user', 'content': question_en})

        _, answer_en = messages.send_message(history=context_history, model=model, stream=False)
        context_history.append({'role': 'assistant', 'content': answer_en})

        if source_code == "en-US":
            answer_final = answer_en
        else:
            answer_final = translate.translate_text(
                text=answer_en, 
                source_lang="English", source_code="en-US", 
                target_lang=source_lang, target_code=source_code
            )
        
        print(f"Assistant: {answer_final}\n")
