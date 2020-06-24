from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding, Conv1D, GlobalMaxPooling1D
from keras.datasets import imdb


# Ignore  the warnings
import warnings
warnings.filterwarnings('always')
warnings.filterwarnings('ignore')


#keras
import keras

from keras.models import Sequential
from keras.layers import Dense , Flatten ,Embedding,Input
from keras.models import Model

import numpy as np
# save np.load
np_load_old = np.load

# modify the default parameters of np.load
np.load = lambda *a, **k: np_load_old(*a, allow_pickle=True, **k)

max_features = 5000
maxlen = 100
batch_size = 64
embedding_dims = 32
filters = 128
kernel_size = 3
#hidden_size = 128
epochs = 5

(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=max_features)

# restore np.load for future normal usage
np.load = np_load_old

print(len(x_test[0]))

# for sample in range(10):
# 	print(x_test[sample])
#
x_train = sequence.pad_sequences(x_train, maxlen=maxlen)
#
#
model = Sequential()
model.add(Embedding(max_features, embedding_dims, input_length=maxlen))
model.add(Conv1D(filters, kernel_size, padding='valid', activation='relu', strides=1))
model.add(GlobalMaxPooling1D())
model.add(Dense(128, activation='sigmoid'))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])

model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs)

model.save("model.h5")
print("Saved model to disk")

########################################################################
# 6. use model
print("New review: \'the movie was a great waste of my time\'")
d = imdb.get_word_index()
review = "the movie was a great waste of my time"

words = review.split()
review = []
for word in words:
  if word not in d:
    review.append(2)
  else:
    review.append(d[word]+3)


review = sequence.pad_sequences([review],
  truncating='pre', padding='pre', maxlen=maxlen)
prediction = model.predict(review)
print("Prediction (0 = negative, 1 = positive) = ", end="")
print("%0.4f" % prediction[0][0])