import unittest

from textStatistics import (
    transform_text,
    find_sentences,
    count_declarartive_sentences,
    count_words_size,
    top_k_ngramms
)


class TestSentencesCount(unittest.TestCase):
    def test_zero_result(self):
        self.assertEqual(len(find_sentences(transform_text(""))), 0)

    def test_one_sentence(self):
        self.assertEqual(len(find_sentences(transform_text("Hellow, world!"))), 1)
        self.assertEqual(len(find_sentences(transform_text("A..."))), 1)

    def test_abbreviations(self):
        self.assertEqual(len(find_sentences(transform_text("Hello, Mr. Max and etc guests. I'm a chinese dawg."))), 2)


class TestNonDeclarativeSentences(unittest.TestCase):
    def test_zero_result(self):
        text = "Evening was chill..."
        self.assertEqual((len(find_sentences(transform_text(text)))) - count_declarartive_sentences(
            find_sentences(transform_text(text))), 0)

    def test_zero_result(self):
        text = "Evening was chill. Was it for you so?"
        self.assertEqual((len(find_sentences(transform_text(text)))) - count_declarartive_sentences(
            find_sentences(transform_text(text))), 1)

    def test_many_result(self):
        text = "A? B? C? F? A! E! F?"
        self.assertEqual((len(find_sentences(transform_text(text)))) - count_declarartive_sentences(
            find_sentences(transform_text(text))), 7)


class TestWordLength(unittest.TestCase):
    def test_zero_result(self):
        text = " . . . .  . . . . "
        words, avr_length = count_words_size(transform_text(text))
        self.assertEqual(avr_length, 0)
        text = ""
        words, avr_length = count_words_size(transform_text(text))
        self.assertEqual(avr_length, 0)

    def test_one_word(self):
        text = "A. A. A. B?"
        words, avr_length = count_words_size(transform_text(text))
        self.assertEqual(avr_length, 1)

    def test_sentence_with_dates(self):
        text = "Hello, today is 12.12.2012. Numbers are not counted."
        words, avr_length = count_words_size(transform_text(text))
        self.assertEqual(words, ["Hello", "today", "is", "Numbers", "are", "not", "counted"])

    def test_sentence_with_numbers(self):
        text = "Hello, today is 21283128731287372183613. Numbers are not counted."
        words, avr_length = count_words_size(transform_text(text))
        self.assertEqual(words, ["Hello", "today", "is", "Numbers", "are", "not", "counted"])


class TestTopKNGrams(unittest.TestCase):

    def test_zero_result(self):
        text = ""
        words, avr_length = count_words_size(transform_text(text))
        top_ngrams = top_k_ngramms(words)
        self.assertEqual(top_ngrams[0], [])

        text = "12 123 123 12 312 3. 12312 1212!"
        words, avr_length = count_words_size(transform_text(text))
        top_ngrams = top_k_ngramms(words)
        self.assertEqual(top_ngrams[0], [])

    def test_many_ngrams(self):
        # The method will find that n-grams that are used beforehand in the text. So in this text there are more than
        # 1 2-gram that have 2 appearances but there counted 'little lamb' because its first appearance is earlier than
        # others 2grams.

        text = "Mary had a little lamb, its fleece was white as snow. And everywhere that Mary went, the lamb was " \
               "sure to go. It followed her to school one day, which was against the rule. It made the children laugh " \
               "and play, to see a lamb at school. When Mary had to go home, the lamb followed her too. Mary had to " \
               "hide the lamb from her father, who said it was not allowed. But Mary loved her little lamb and " \
               "couldn't bear to be apart from it."
        words, avr_length = count_words_size(transform_text(text))
        top_ngrams = top_k_ngramms(words, 3, 2)
        self.assertEqual(top_ngrams[0], [('Mary had', 3), ('the lamb', 3), ('little lamb', 2)])
