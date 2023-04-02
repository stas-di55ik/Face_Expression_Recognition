from deep_translator import GoogleTranslator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def auto_translate_to_en(source_text):
    return GoogleTranslator(source='auto', target='en').translate(source_text)


def get_sentiment_analysis(en_text):
    sentiment = SentimentIntensityAnalyzer()
    score = sentiment.polarity_scores(en_text)
    print(score)
    return str(score)
