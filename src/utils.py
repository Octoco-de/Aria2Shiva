async def constrain_text_to_length(text, length):
    result = text
    if len(result) > length:
        result = f"{result[:length]}..."
    return result
