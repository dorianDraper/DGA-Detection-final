import streamlit as st
import tldextract
import regex as re
import pandas as pd
import numpy as np
from pickle import load, dump
from collections import Counter


def extract_subdomain_and_domain(host):
    ext = tldextract.extract(host)
    return ext.domain if ext.subdomain == '' else '.'.join([ext.subdomain, ext.domain])

def get_domain_length(host):
    return len(host)

def unique_char_count(host):
    return len(set(host))

def unique_letter_count(host):
    return len(set(re.sub(r'[^a-z]', '', host)))

def unique_digit_count(host):
    return len(set(re.sub(r'[^0-9]', '', host)))

def consonant_ratio(host):
    consonants = sum(1 for char in host if char.isalpha() and char.lower() not in 'aeiou')
    return consonants / len(host) if host else 0

def vowel_ratio(host):
    vowels = sum(1 for char in host if char.lower() in 'aeiou')
    return vowels / len(host) if host else 0

def longest_consonant_string(host):
    consonants = 'bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ'
    max_length = 0
    current_length = 0
    for char in host:
        if char in consonants:
            current_length += 1
            max_length = max(max_length, current_length)
        else:
            current_length = 0
    return max_length

def entropy(host):
    p, lns = Counter(host), float(len(host))
    return -sum( count/lns * np.log2(count/lns) for count in p.values())


stopwords = load(open('../data/raw/top_english_words.pkl', 'rb'))
dict_freq = { word[0]: num for num, word in enumerate(stopwords.values, 1) }

def ngrams(word, n):
    l_ngrams = []
    n = n if isinstance(n, list) else [n]
    word = word if isinstance(word, list) else [word]

    for w in word:
        for curr_n in n:
            ngrams = [w[i:i+curr_n] for i in range(0,len(w)-curr_n+1)]
            l_ngrams.extend(ngrams)
    return l_ngrams

def ngram_feature(host, n):
    l_ngrams = ngrams(host, n)
    count_sum = sum(dict_freq.get(ngram, 0) for ngram in l_ngrams)
    feature = count_sum/(len(host)-n+1) if len(host)-n+1 else 0
    return feature

def average_ngram_feature(l_ngram_feature):
    return sum(l_ngram_feature)/len(l_ngram_feature) if l_ngram_feature else 0


model = load(open('../models/xgb_clf_opt.pkl', 'rb'))

st.title("DGA Detector")
host = st.text_input("Enter domain name:")
df = pd.DataFrame([])

if st.button("Is it legit or DGA-generated?"):
    domain = extract_subdomain_and_domain(host)
    df['long_consonant_str'] = [longest_consonant_string(domain)]
    df['unique_char_count'] = [unique_char_count(domain)]
    df['entropy'] = [entropy(domain)]
    df['vowel_ratio'] = [vowel_ratio(domain)]
    df['unique_letter_count'] = [unique_letter_count(domain)]
    df['d_length'] = [get_domain_length(domain)]
    df['consonant_ratio'] = [consonant_ratio(domain)]
    df['unique_digit_count'] = [unique_digit_count(domain)]
    df['ngrams'] = [average_ngram_feature([ngram_feature(domain, n) for n in [1,2,3]])]
    
    prediction = model.predict(df)
    if prediction[0] == 1:
        st.write("This is DGA-generated")
    else:
        st.write("This is a legit domain")
    

