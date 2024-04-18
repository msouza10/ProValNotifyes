from discord_client import bot  # Importa a instância do bot configurada
from dotenv import load_dotenv
import os

def main():
    load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env
    token = os.getenv('DISCORD_TOKEN')  # Obtém o token do bot de forma segura

    if token is None:
        raise ValueError("Bot token not found. Please set up your .env file correctly.")

    bot.run(token)

if __name__ == '__main__':
    main()
