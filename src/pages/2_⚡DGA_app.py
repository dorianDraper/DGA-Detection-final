import streamlit as st
import tldextract
import regex as re
import requests
import json
import pandas as pd
import numpy as np
from pickle import load, dump
from collections import Counter

st.set_page_config(page_title="DGA Detector", 
                   page_icon="⚡", 
                   layout="centered") 

st.markdown(
    """
    This app is a DGA detector. It uses a machine learning model to predict if a domain is legit ✅ or DGA-generated ❌. 
    Please enter a domain name in the text box and click the button to check the prediction.
"""
)

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

api_key = "7604f0fccda6cd86ab26"

def submit_dga_domain(domain):
    url = 'https://urlhaus.abuse.ch/api/'
    json_data = {
        'token': api_key,
        'anonymous': '0',
        'submission': [
            {
                'url': domain,
                'threat': 'malware_download'
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, json=json_data, timeout=15)
        if response.status_code == 200:
            return response.content
        else:
            return f"Error: {response.status_code} - {response.reason}"
    except Exception as e:
        return f"Error: {str(e)}"

def validate_domain(domain):
    # Regular expression for domain name validation
    domain_regex = r"^(?!:\/\/)(?!www\.)([a-zA-Z0-9][a-zA-Z0-9-]{0,61}[a-zA-Z0-9]\.)+[a-zA-Z]{2,}$"
    if re.match(domain_regex, domain):
        return True
    else:
        return False

if st.button("Is it legit or DGA-generated?"):
    if host.strip() == '':
        st.warning("Please enter a domain name.")
    elif not validate_domain(host):
        st.warning("Please enter a valid domain name (e.g., example.com).")
    else:
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
        probability = model.predict_proba(df)
        if prediction[0] == 1:
            st.write(f"The domain name :red['_{host}_'] is DGA-generated with a probability of %.2f%%" % (probability[0][1] * 100))
            st.markdown("""
                        You can submit this domain to URLhaus. [URLhaus](https://urlhaus.abuse.ch/about/) is a project operated by abuse.ch. 
                        The purpose of the project is to collect, track and share malware URLs, helping 
                        network administrators and security analysts to protect their network and customers 
                        from cyber threats.""")
            if st.button("Submit DGA-generated domain to URLhaus"):
                response = submit_dga_domain(domain)
                st.write(response)
        else:
            st.write("This is a legit domain")


st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center; margin-top: 150px;">
        <span style="margin-right: 20px;">© Powered & Developed by <b>Jorge Payà</b></span>
    </div>
    """, unsafe_allow_html=True)