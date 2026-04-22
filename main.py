from Core.Brain import processar_conversa
from voz import criar_audio

def chat():
    print("--- Nous Inicializado ---")
    
    while True:
        user_input = input("\nAinas: ")
        if user_input.lower() in ['sair', 'exit']: 
            print("Encerrando Modulo de conversa.")
            break
        
        try:
            # Chama o cérebro
            stream = processar_conversa(user_input)
            content = ''

            print(f'\n\nNous: {stream}\n', end='', flush=True)
            
                    
            # criar_audio(stream)

        except Exception as e:
            print(f"\n[ERRO DE SISTEMA]: {e}")

if __name__ == "__main__":
    chat()