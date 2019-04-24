from textblob import TextBlob


def get_sentiments(text):
	sentiment = TextBlob(text).sentiment.polarity
	positive = 50
	negative = 50
	sentiment *= 50
	positive += sentiment
	negative -= sentiment
	return positive, negative

