import tiktoken

def encode_decode(text: str, model: str = "gpt-3.5-turbo"):
    """
    Encode and decode text using the tokenizer for the specified model.

    :param text: The input text to be tokenized.
    :param model: The model name whose tokenizer to use (default is "gpt-3.5-turbo").
    """
    # Get encoding for the model
    encoding = tiktoken.encoding_for_model(model)

    # Encode: text -> token IDs
    tokens = encoding.encode(text)
    print("Tokens:", tokens)
    print("Token count:", len(tokens))

    # Decode: token IDs -> text
    decoded_text = encoding.decode(tokens)
    print("Decoded:", decoded_text)


if __name__ == "__main__":
    sample_text = "Hello, how are you?"
    encode_decode(sample_text)
