import re

def transform_text(text):
    if(len(re.findall(r'[^\x00-\x7F]+', text))):  # Only latin letters, numbers and separators
        raise Exception('Only Latin letters, numbers and separators can be processed!')
    return text

def count_sentences(text):
    sentences = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)
    
    return sentences