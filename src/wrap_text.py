import shutil
import textwrap

def wrap_text(text):
    width = shutil.get_terminal_size(fallback=(100, 20)).columns
    return textwrap.fill(text, width=width, break_long_words=False)