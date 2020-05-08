
import os
import pytesseract
import string
import cv2
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

stopwords = []

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

with open(dir_path + '/stopwords.txt', 'r') as stopword_file:
    stopwords = stopword_file.readlines()

pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

def compare_img(img1_file, img2_file):
    """Return the cosine similarity of two images' text."""
    img1 = cv2.imread(img1_file)
    img2 = cv2.imread(img2_file)
    img1_text = get_img_text(img1)
    img2_text = get_img_text(img2)
    combined_text = [
        img1_text,
        img2_text,
    ]
    vectors = CountVectorizer().fit_transform(combined_text).toarray()
    return _cosine_sim_vectors(vectors[0], vectors[1])

def get_text_comp(text1, text2):
    """Return the cosine similarity of two strings"""
    combined_text = [
        text1,
        text2,
    ]
    vectors = CountVectorizer().fit_transform(combined_text).toarray()
    return _cosine_sim_vectors(vectors[0], vectors[1])


def get_img_text(img_file):
    """Get cleaned text from image."""
    img = cv2.imread(img_file)
    img_text = pytesseract.image_to_string(img)
    return _clean_string(img_text)

def _clean_string(text):
    """Remove punctuation and stop words from string."""
    text = ''.join([word for word in text if word not in string.punctuation])
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in stopwords])

    return text

def _cosine_sim_vectors(vec1, vec2):
    """Return the cosine similarity of two vectors."""
    vec1 = vec1.reshape(1, -1)
    vec2 = vec2.reshape(1, -1)
    return cosine_similarity(vec1, vec2)[0][0]