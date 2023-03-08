import re
from collections import Counter

def transform_text(text):
    # Only latin letters, numbers and separators
    if len(re.findall(r'[^\x00-\x7F]+', text)):
        raise Exception(
            'Only Latin letters, numbers and separators can be processed!')
    return text


def find_sentences(text):
    sentences = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)

    return sentences


def count_declarartive_sentences(sentences):
    return len([dec_sentence for dec_sentence in sentences if dec_sentence.endswith('.') or dec_sentence.endswith('...')])


def count_words_size(text):
    words = re.findall(r'\b(?![.,\d])\w*[a-zA-Z]\w*\b', text)

    sum_letters = 0
    for word in words:
        sum_letters += len(word)

    return words, sum_letters/len(words)


def count_sentence_length(words, sentences):
    sum_of_letters = 0
    for word in words:
        sum_of_letters += len(word)

    return sum_of_letters/len(sentences)

def top_k_ngramms(words, K=10, N=4):
    ngrams = []
    for i in range(len(words) - N + 1):
        ngram = " ".join(words[i:i+N])
        ngrams.append(ngram)    

    top_ngrams = Counter(ngrams).most_common(K)

    return top_ngrams, K, N
