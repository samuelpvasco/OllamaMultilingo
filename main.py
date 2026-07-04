import app.messages as messages
import app.chat as chat

def main():
    try:
        model = messages.get_models()
    
        chat.chat_talk(model=model)
        
    except:
        print('An unexpected error ocurred, try again later')
    
    
main()