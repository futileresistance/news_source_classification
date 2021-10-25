from bs4 import BeautifulSoup
import numpy as np
import requests
import re

def mean_li(soup):
    lis = []
    for item in soup.find_all('ul'):
        new_bs = BeautifulSoup(str(item),features='html.parser')
        lis_num = len(new_bs.find_all('li'))
        if lis_num:
            lis.append(lis_num)
    if lis:
        return int(np.mean(lis))
    else:
        return 0


def href_counter(html_page):
    urls = re.findall(r'href=[\'"]?([^\'" >]+)', html_page.text)
    pattern = r'.php|css|json|xml|mailto|jpg|png|jpeg'
    filtered = [val for val in urls if not re.search(pattern, val)]
    return len(filtered)

def get_feats(soup_page):
    news_pat = r'<.*news.*>'
    a_and_p_pat = r'<a.*>[\S\n\t\v ]?<p'
    div_and_h_pat = r'<div.*>[\S\n\t\v ]?<h.?'
    a_and_div_pat = r'<a.*>[\S\n\t\v ]?<div'
    h_and_a_pat = r'<h.*>[\S\n\t\v ]?<a'
    img_and_a_pat = r'<img.*>[\S\n\t\v ]?<a'
    ###
    a_counter = len(soup_page.find_all('a'))
    div_counter = len(soup_page.find_all('div'))
    li_counter = len(soup_page.find_all('li'))
    ul_counter = len(soup_page.find_all('ul'))
    nav_counter = len(soup_page.find_all('nav'))
    ###
    script_counter = len(soup_page.find_all('script'))
    h_counter = len(soup_page.find_all('h'))
    h1_counter = len(soup_page.find_all('h1'))
    h2_counter = len(soup_page.find_all('h2'))
    img_counter = len(soup_page.find_all('img'))
    ###
    p_counter = len(soup_page.find_all('p'))
    link_counter = len(soup_page.find_all('link'))
    button_counter = len(soup_page.find_all('button'))
    span_counter = len(soup_page.find_all('span'))
    ###
    li_mean = mean_li(soup_page)
    href_count = href_counter(soup_page)
    ###
    news_counter = len(re.findall(news_pat, str(soup_page.html)))
    a_and_p_regex = len(re.findall(a_and_p_pat, str(soup_page.html)))
    div_and_h_regex = len(re.findall(div_and_h_pat, str(soup_page.html)))
    a_and_div_regex = len(re.findall(a_and_div_pat, str(soup_page.html)))
    h_and_a_regex = len(re.findall(h_and_a_pat, str(soup_page.html)))
    img_and_a_regex = len(re.findall(img_and_a_pat, str(soup_page.html)))

    return [a_counter, div_counter, li_counter, ul_counter, nav_counter, \
            script_counter, h_counter, h1_counter, h2_counter, img_counter, \
            p_counter, link_counter, button_counter, span_counter, \
            li_mean, href_count, \
            news_counter, a_and_p_regex, div_and_h_regex, a_and_div_regex, h_and_a_regex, img_and_a_regex]

def get_pattern(page):
    pat = r'title="([\S\n\t\v ]*?)"'
    items = re.findall(pat, str(page.html))
    new_items = set(items)
    return list(new_items)


len_2 = lambda x: True if len(x) else False
len_3 = lambda x: True if len(x) > 2 else False

def remove_special_characters(text):
    # define the pattern to keep
    pat = r'[^a-zA-z0-9а-яА-я.,!?/:;\"\'\s)(«»]'
    return re.sub(pat, '', text.lower())

def make_words_list(items):
    words = []
    for item in items:
        word_list = item.split()
        words.extend(word_list)
    return list(set(words))


def get_title_text(soup_page):
    items = get_pattern(soup_page)
    items = list(map(remove_special_characters, items))
    words = make_words_list(items)
    return list(filter(len_3, words[:300]))


def get_img_text(soup):
    cleaned = re.sub(r'[\n\t\d\.\-)("«»]', ' ', soup.text)
    texts = ' '.join(cleaned.split()).lower().split()
    return list(filter(len_3, texts[:300]))


def clean_html(soup):
    cleaned = re.sub(r'[\n\t\.)(]', ' ', str(soup.html))
    cleaned = ' '.join(cleaned.split())
    return cleaned

def get_html_and_text_data(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    max_html_size = 150000
    if url[:4] != 'http':
        url = 'https://' + url
    try:
        page = requests.get(url, verify = False, timeout = 10, headers=headers)
    except:
        print('request failed', url,'--'*10)
    soup = BeautifulSoup(page.text, features='html.parser')
    soup = BeautifulSoup(clean_html(soup), features='html.parser')
    #string_power = len(str(soup.html))
    #if string_power > max_html_size:
    #    soup = BeautifulSoup(str(soup.html)[:max_html_size], features='html.parser')
    html_feats = get_feats(soup)
    title_text = get_title_text(soup)
    image_text = get_img_text(soup)
    return html_feats, title_text+image_text