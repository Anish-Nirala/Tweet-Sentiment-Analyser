from textblob import TextBlob


class Polarity:
    def __init__(self) -> None:
        pass

    def get_polarity(self, text):
        textblob = TextBlob(str(text))
        pol = textblob.sentiment.polarity
        if(pol == 0):
            return "Neutral"
        elif(pol > 0 and pol <= 0.3):
            return "Weakly Positive"
        elif(pol > 0.3 and pol <= 0.6):
            return "Positive"
        elif(pol > 0.6 and pol <= 1):
            return "Strongly Positive"
        elif(pol > -0.3 and pol <= 0):
            return "Weakly Negative"
        elif(pol > -0.6 and pol <= -0.3):
            return "Negative"
        elif(pol > -1 and pol <= -0.6):
            return "Strongly Negative"
