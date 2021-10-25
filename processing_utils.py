import numpy as np

def prepare_html_feats(html_feats):
    html_feats = np.array(html_feats)
    html_feats = np.reshape(np.expand_dims(html_feats,-1), (1,22))
    return html_feats

def prepare_text_feats(text, countvect, tfidf):
    text = ' '.join(text)
    transformed_test = countvect.transform([text])
    text_feats = np.array(tfidf.transform(transformed_test).todense())
    return text_feats

def combine_feats(text_feats, html_feats):
    vec = np.hstack([text_feats, html_feats])
    return vec

def make_predict(url, parse_func, model, counter, tfidf):
    tags, texts = parse_func(url)
    tags = prepare_html_feats(tags)
    texts = prepare_text_feats(texts,counter,tfidf)
    emb_vector = combine_feats(texts, tags)
    _,  prediction = model.predict_proba(emb_vector)[0]
    if prediction > 0.5:
        return 1, prediction
    else:
        return 0, prediction