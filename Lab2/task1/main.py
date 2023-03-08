import textStatistics

text = input('Enter text:')

text= textStatistics.transform_text(text)
sentences = textStatistics.find_sentences(text)
declarative_sentences = textStatistics.count_declarartive_sentences(sentences)
print(declarative_sentences)
print(textStatistics.count_words_size(text))