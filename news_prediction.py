from model import vectorizer, tfidf, catboost
from parse_utils import get_html_and_text_data
from processing_utils import make_predict


if __name__ == '__main__':
    url = 'meduza.io'
    prediction, prob = make_predict(url, get_html_and_text_data, catboost, vectorizer, tfidf)
    print(url, prediction)
