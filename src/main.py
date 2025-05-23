# filepath: /agent-oai-sdk/agent-oai-sdk/src/main.py
from config.env import config

def load_env():
    print("API_KEY:", config.OPENAI_KEY)
    

def main():
    # Load environment variables
    load_env()

    # Initialize the OpenAI API client
    print("🪁 done... ")

if __name__ == "__main__":
    main()