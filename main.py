from functions import messages
from functions import chat

def main():
    try:
        model = messages.get_models()
    
        chat.chat_talk(model=model)
    except:
        print('An unexpected error ocurred, try again later')
    
    
main()