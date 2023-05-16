"""Utilities to help processing chatbot prompts or answers."""


def keep_first_line(text: str) -> str:
    r"""Truncate a string to the first non-empty line.

    Examples
    --------
    >>> keep_first_line("\nFirst line.\nSecond line.")
    'First line.'
    """
    return text.lstrip("\n").split("\n")[0].strip(" ")


def drop_if_keyword(text: str, keyword: str = "Not found.") -> str:
    """If input keyword occurs in text, replace it with the keyword.

    Examples
    --------
    >>> drop_if_keyword("Not found. Some made up answer.", keyword="Not found.")
    'Not found.'
    """
    if keyword in text:
        return keyword
    return text


def post_process_answer(answer: str) -> str:
    """Post-process an answer by keeping only the first line and dropping
    it if it contains the keyword 'Not found.'."""
    text = keep_first_line(answer)
    text = drop_if_keyword(text)
    return text
