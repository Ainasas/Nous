from Core.Brain import processar_conversa, salvar_interacao

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
            
            print("Nous: ", end="", flush=True)
            full_response = ""
            
            # A Interface decide como exibir (no terminal, é via print)
            for chunk in stream:
                content = chunk['message']['content']
                print(content, end="", flush=True)
                full_response += content
            
            print()
            
            # Após o fim da resposta, salva a memória
            salvar_interacao(user_input, full_response)

        except Exception as e:
            print(f"\n[ERRO DE SISTEMA]: {e}")

if __name__ == "__main__":
    chat()