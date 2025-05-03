from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import pickle
import re
import os
from bnltk.stemmer import BanglaStemmer


with open('core/trained_model.pkl', 'rb') as f:
    data = pickle.load(f)
    model = data['model']
    vectorizer = data['vectorizer']



prthomalo="https://www.prothomalo.com/"
prthomaloClass="tilte-no-link-parent"

bdpratidin="https://www.bd-pratidin.com/"
bdpratidinClass="fs-2 mt-3 mt-lg-0"
kalerkontho="https://www.kalerkantho.com/"
kalerkonthoClass="d-none d-sm-block text-break"

def streamming(text):
    cleanText = re.sub(r'[^\u0980-\u09FF\s]', '', text)  
    cleanText = cleanText.split()
    stemmer = BanglaStemmer()
    # When I use stopwords, the prediction accuracy becomes lower.
    # cleanText = [stemmer.stem(word) for word in cleanText if word not in stopwords.words('bengali')]
    cleanText = [stemmer.stem(word) for word in cleanText]
    return ' '.join(cleanText)

def predict_sentiment(text):
    processed_text = streamming(text)
    text_vector = vectorizer.transform([processed_text])
    prediction = model.predict(text_vector)[0]

    if prediction == 1:
        return "Neutral"
    elif prediction == 2:
        return "Positive"
    else:
        return "Negative"


def home(request):
    final = None
    result=None
    news_url=None
    newsTitle=None
    cls=None


    if request.method == "POST":
        value = request.POST.get('value')
        if value == '1':
            news_url=prthomalo
            cls=prthomaloClass

        elif value == '2':
            news_url=bdpratidin
            cls=bdpratidinClass
        elif value =='3':
            news_url=kalerkontho
            cls=kalerkonthoClass
        else:
            news_url=None 
            cls=None   
        

        try:
           
            res = requests.get(news_url, timeout=5)
            soup = BeautifulSoup(res.text, 'html.parser')
            extTitle=soup.find(class_=cls)
            newsTitle=extTitle.text 
            result = predict_sentiment(newsTitle)
            
                 
        except Exception as e:
            newsTitle = "SomeThing Wrong"

    return render(request, 'index.html', {
        'url':news_url,
        'title': newsTitle,
        'result': result,
    })

