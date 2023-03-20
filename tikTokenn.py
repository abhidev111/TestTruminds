import tiktoken

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

def get_token_size(paragraph):
    return len(encoding.encode(paragraph))
