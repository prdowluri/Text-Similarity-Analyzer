# -*- coding: utf-8 -*-
"""Semantic_Similarity.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NmdlsaoZKGEKXAspEcM5nr1JebCGxyNz

# Semantic Similarity between Paragraphs or Sentences

# Part A: Task Description:
 The task at hand involves evaluating the semantic similarity between two paragraphs. Semantic Textual Similarity (STS) measures the extent to which two pieces of text convey similar meanings. STS entails assesses the degree to which two sentences are semantically equivalent to each other. Our task is to involves the producing real-valued similarity scores for sentence pairs.


# Description of the Data:

 The dataset comprises pairs of paragraphs randomly selected from a larger raw dataset. These paragraphs may or may not exhibit semantic similarity. Participants are tasked with predicting a value ranging from 0 to 1, which indicates the degree of similarity between each pair of text paragraphs. A score of

-  1 means highly similar
-  0 means highly dissimilar

# Approach to solve this problem:
To solve this Natural Language Processing (NLP) problem, the initial step involves text embedding, a pivotal aspect in building deep learning models. Text embedding transforms textual data (such as sentences) into numerical vectors.

Once the sentences are converted into vectors, we can calculate how close these vectors are based on the cosine similarity.

We are not converting just based on keyword. Here, we need to concentrate the context and meaning of the text.

To address this, we leverage the Universal Sentence Encoder (USE). This encoder translates text into higher-dimensional vectors, which are ideal for our semantic similarity task. The pre-trained Universal Sentence Encoder (USE) is readily accessible through TensorFlow Hub, providing a robust solution for our needs.

"""
"""Step-1: Install the required libraries or Packeges
"""

# !pip install -q tensorflow tensorflow_hub pandas

"""Step-2: Importing required libraries:

 Let's import the necessary libraries and load the TensorFlow Hub module for the Universal Sentence Encoder.
"""

import tensorflow as tf       # To work with USE4
import pandas as pd           # To work with tables
import tensorflow_hub as hub  # contains USE4
module_url = "https://tfhub.dev/google/universal-sentence-encoder/4" #Model is imported from this URL
model = hub.load(module_url)
def embed(input):
  return model(input)

"""Step-3: Reading Data"""

data = pd.read_csv("/content/DataNeuron_Text_Similarity.csv")

data.head()

data.shape

data['text1'][0]

type(data['text1'][0]) # we can see that all the data is in string type

""" Step-4: Encoding text to vectors:
We have used USE version 4.
It is trained on the whole wikipedia data.
Our Sentence have a sequence of words. we give this sentence to our model (USE4), it gives us a "dense numeric vector".
Here, we passed sentence pair and got a vector pair.
"""

message = [data['text1'][0], data['text2'][0]]
message_embeddings = embed(message)
message_embeddings

type(message_embeddings)

""" Here we can see that the type of the vector retured is tensorflow.python.framework.ops.EagerTensor so, we cannot directly use it to compute the cosine similarity. We need to convert it into a numpy array first.
"""

type(message_embeddings[0])

type(tf.make_ndarray(tf.make_tensor_proto(message_embeddings)))

a_np = tf.make_ndarray(tf.make_tensor_proto(message_embeddings))

""" Step-5: Finding Cosine similarity
We ran a for loop for all the sentence pair present in our data and found the vector representation of our sentences. For each vector pair, we found the cosine between the by using usual cosine formula.
i.e.  

 Cosine Similarity = Dot(a,b)/norm(a)*norm(b)

We get the value ranging from -1 to 1. But, we need values ranging from 0 to 1 hence we will add 1 to the cosine similarity value and then normalizze it.
"""

from numpy import dot                                           # To calculate the dot product of two vectors
from numpy.linalg import norm                                   # For finding the norm of a vector

ans = []                                                        # This list will contain the cosin similarity value for each vector pair present.
for i in range(len(data)):
  messages = [data['text1'][i], data['text2'][i]]               # Storing each sentence pair in messages
  message_embeddings = embed(messages)                          # Converting the sentence pair to vector pair using the embed() function
  a = tf.make_ndarray(tf.make_tensor_proto(message_embeddings)) # Storing the vector in the form of numpy array
  cos_sim = dot(a[0], a[1])/(norm(a[0])*norm(a[1]))             # Finding the cosine between the two vectors
  ans.append(cos_sim)                                           # Appending the values into the ans list

len(ans)

""" Step-6: To get the scores and save the file in CSV format."""

# Converting the ans list into Dataframe so that we can add it to our "data"
Answer = pd.DataFrame(ans, columns = ['Similarity_Score'])

Answer.head()

data = data.join(Answer)  # Joining the Similarity_Score Dataframe (Ans) to our main Data

data.head()

# Adding 1 to each of the values of Similarity_Score to make the values from 0 to 2. (Initially it was from [-1,1])
data['Similarity_Score'] = data['Similarity_Score'] + 1

data.head()

# Normalizing the Similarity_Score to get the value between 0 and 1
data['Similarity_Score'] = data['Similarity_Score']/data['Similarity_Score'].abs().max()

data.head()

data.insert(0, 'Unique_ID', range(1, len(data) + 1))

data.head()

# # Similarity_Score

# from matplotlib import pyplot as plt
# data['Similarity_Score'].plot(kind='line', figsize=(8, 4), title='Similarity_Score')
# plt.gca().spines[['top', 'right']].set_visible(False)

data['Unique_ID'].shape

Submission_task = data[['Unique_ID', 'Similarity_Score']]

Submission_task.head()

Submission_task.set_index("Unique_ID", inplace = True)

from google.colab import files
Submission_task.to_csv('Submission_Task.csv')
files.download('Submission_Task.csv')