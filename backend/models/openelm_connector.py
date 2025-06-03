from mlx_lm import generate, load

# Global variables for model and tokenizer
model = None
tokenizer = None

def initialize_openelm_model(checkpoint="mlx-community/OpenELM-450M-instruct-8bit"):
    global model, tokenizer
    # Load the model and tokenizer only once
    if model is None or tokenizer is None:
        model, tokenizer = load(path_or_hf_repo=checkpoint)

def process_user_query(query, temp=0.7, max_tokens=1000):
    """
    query: str, the user's message
    Returns: str, the model's response
    """
    global model, tokenizer
    if model is None or tokenizer is None:
        raise RuntimeError("Model not initialized. Call initialize_openelm_model() first.")

    # Prepare conversation history (single-turn for now)
    conversation = [{"role": "user", "content": query}]
    prompt = tokenizer.apply_chat_template(
        conversation=conversation, tokenize=False, add_generation_prompt=True
    )

    generation_args = {
        "temp": temp,
        "repetition_penalty": 1.2,
        "repetition_context_size": 20,
        "top_p": 0.95,
    }

    response = generate(
        model=model,
        tokenizer=tokenizer,
        prompt=prompt,
        max_tokens=max_tokens,
        verbose=False,
        **generation_args,
    )
    return response

def query_openelm(user_question):
    """
    Wrapper for process_user_query for compatibility.
    """
    return process_user_query(user_question)