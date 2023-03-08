import re

def transform_text(text):
    if(len(re.findall(r'[^\x00-\x7F]+', text))):  # Only latin letters, numbers and separators
        raise Exception('Only Latin letters, numbers and separators can be processed!')
    return text

def find_sentences(text):
    sentences = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)
    
    return sentences

def count_declarartive_sentences(sentences):
    return len([dec_sentence for dec_sentence in sentences if dec_sentence.endswith('.') or dec_sentence.endswith('...')])


def count_words_size(text):
    words = re.findall(r'\b(?![.,\d])\w*[a-zA-Z]\w*\b', text)

    sum_letters=0
    for word in words:
        sum_letters+=len(word)
    
    return sum_letters/len(words)

