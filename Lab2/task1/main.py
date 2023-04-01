import textStatistics

text = input('Enter text:')
N = input('Enter N:')
K = input('Enter K:')
flag = False
try: 
    N = int(N)
    K = int(K)
except ValueError:
    flag = True 

text = textStatistics.transform_text(text)
print(text)
sentences = textStatistics.find_sentences(text)
declarative_sentences_length = textStatistics.count_declarartive_sentences(sentences)

non_declarative_sentences_length = len(sentences) - declarative_sentences_length

words, avr_length = textStatistics.count_words_size(text)
avr_sentence_length = textStatistics.count_sentence_length(words, sentences)

if flag:
    top_ngrams, N, K = textStatistics.top_k_ngramms(words)   
else:
    top_ngrams, N, K = textStatistics.top_k_ngramms(words, N, K)   
    

print(f'Amount of sentences: {len(sentences)}')
print(f'Amount of non-declarative sentences: {non_declarative_sentences_length}')
print(f'Average length of the sentence: {avr_sentence_length}')
print(f'Average length of the word: {avr_length}')
print(f"Top {K} repeated {N}-grams:")
for ngram, count in top_ngrams:
    print(f"{ngram}: {count}")
