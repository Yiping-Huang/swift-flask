from mlx_lm import generate, load
from mlx_lm.sample_utils import make_sampler

# Global variables for model and tokenizer
model = None
tokenizer = None

def initialize_openelm_model(checkpoint="mlx-community/OpenELM-270M-Instruct"):
    global model, tokenizer
    # Load the model and tokenizer only once
    if model is None or tokenizer is None:
        model, tokenizer = load(path_or_hf_repo=checkpoint)


def process_user_query(query, temp=0, top_p=0.1, top_k=5, max_tokens=512):
    global model, tokenizer
    if model is None or tokenizer is None:
        raise RuntimeError("Model not initialized. Call initialize_openelm_model() first.")

    prompt =  'User question:' + query + 'Answer me within 500 words. Your Answer:'

    sampler = make_sampler(
        temp=temp,
        top_p=top_p,
        min_p=0.0,
        min_tokens_to_keep=1,
        top_k=top_k,
        xtc_probability=0.0,
        xtc_threshold=0.0,
        xtc_special_tokens=tokenizer.encode("\n") + list(tokenizer.eos_token_ids),
    )

    response = generate(
        model=model,
        tokenizer=tokenizer,
        prompt=prompt,
        max_tokens=max_tokens,
        sampler=sampler,
        verbose=False,
    )
    return response

def query_openelm(user_question):
    """
    Wrapper for process_user_query for compatibility.
    """
    return process_user_query(user_question)