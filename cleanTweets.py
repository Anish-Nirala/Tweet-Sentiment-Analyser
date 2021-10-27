import re


class cleanTweets:
    def __init__(self) -> None:
        pass

    def clean_text(self, text):
        return ' '.join(re.sub("(@[a-zA-Z0-9]+)|([^0-9A-Za-z])|(https://[\w.]+/[\w]+)", " ", text).split())

    def drop_numbers(self, text):
        new_text = []
        for i in text:
            if not re.search('\d', i):
                new_text.append(i)
        return ''.join(new_text)
