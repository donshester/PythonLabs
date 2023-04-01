import re
from collections import Counter


def transform_text(text):
    # Only latin letters, numbers and separators
    if len(re.findall(r'[^\x00-\x7F]+', text)):
        raise Exception(
            'Only Latin letters, numbers and separators can be processed!')

    abbreviations = ["Mr.", "Mrs.", "Dr.", "Ms.", "Jr.", "Sr.", "St."]
    for abbr in abbreviations:
        text = text.replace(abbr, abbr[:-1])
    return text


def find_sentences(text):
    if text == "":
        return []
    sentences = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s+(?=[A-Z])', text)

    return sentences


def count_declarartive_sentences(sentences):
    return len(
        [dec_sentence for dec_sentence in sentences if dec_sentence.endswith('.') or dec_sentence.endswith('...')])


def count_words_size(text):
    words = re.findall(r'\b(?![.,\d])\w*[a-zA-Z]\w*\b', text)

    sum_letters = 0
    for word in words:
        sum_letters += len(word)

    try:
        avg_words = sum_letters / len(words)
    except ZeroDivisionError:
        avg_words = 0
    return words, avg_words


def count_sentence_length(words, sentences):
    sum_of_letters = 0
    for word in words:
        sum_of_letters += len(word)

    try:
        sentence_length = sum_of_letters / len(sentences)
    except ZeroDivisionError:
        sentence_length = 0
    return sentence_length


def top_k_ngramms(words, K=10, N=4):
    ngrams = []
    for i in range(len(words) - N + 1):
        ngram = " ".join(words[i:i + N])
        ngrams.append(ngram)

    top_ngrams = Counter(ngrams).most_common(K)

    return top_ngrams, K, N
