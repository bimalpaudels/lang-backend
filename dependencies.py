from core.ai import GPT

# Single Initialization
print("Initializing language model...")
gpt = GPT()


def get_gpt() -> GPT:
    return gpt
