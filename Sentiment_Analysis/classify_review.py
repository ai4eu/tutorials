from keras.preprocessing import sequence
from keras.datasets import imdb
from keras.models import load_model


# Ignore  the warnings
import warnings
warnings.filterwarnings('always')
warnings.filterwarnings('ignore')


def classify_review(review):
	maxlen = 100
	model = load_model('model.h5')
	d = imdb.get_word_index()
	words = review.split()
	review = []
	for word in words:
		if word not in d:
			review.append(2)
		else:
			review.append(d[word] + 3)

	review = sequence.pad_sequences([review],
									truncating='pre', padding='pre', maxlen=maxlen)
	prediction = model.predict(review)
	return prediction[0][0]















