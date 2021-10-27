from nltk.tokenize import word_tokenize


class Lemmatizer:
    def __init__(self) -> None:
        self.lemmatizer = WordNetLemmatizer()

    def lemmatise(self, text):
        text_tokens = word_tokenize(text)
        text_lemm = [self.lemmatizer.lemmatize(word) for word in text_tokens]
        return ' '.join(text_lemm)

    def remove_stopword(self, text):
        text_tokens = word_tokenize(text)
        tokens = [word for word in text_tokens if not word in set(
            stopwords.words('english'))]
        tokens_text = ' '.join(tokens)
        return tokens_text
