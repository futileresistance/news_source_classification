from catboost import CatBoostClassifier
import pickle
import warnings
warnings.filterwarnings('ignore')

vectorizer = pickle.load(open("countvectorizer_NEWS.pickle", "rb"))
tfidf = pickle.load(open("tfidf_NEWS.pickle", "rb"))

catboost = CatBoostClassifier()
catboost.load_model('catboost_model_news_class')
