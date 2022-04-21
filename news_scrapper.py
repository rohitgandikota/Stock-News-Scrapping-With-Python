# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 10:33:23 2022

@author: Rohit Gandikota
"""

from newsapi import NewsApiClient
from bs4 import BeautifulSoup
import json, xml
import requests
from html.parser import HTMLParser
import re  
import itertools
# Generate an API key from https://newsapi.org/register
newsapi = NewsApiClient(api_key = '1fb7eb97ad3e4784a20577e74d320ff3')

def getNews(company, proxies=''):
    
    queries = ['Stock', 'Investors', 'Finances', 'Stock Performance', 'Quaterly Reports', '']
    
    output_obj = []
    titles = []
    for query in queries:
        news = newsapi.get_top_headlines(q=(company+' '+query).strip(), category='business', language='en')
        
        for article in news['articles']:
            if article['title'] not in titles:
                del article['source'], article['author'], article['urlToImage']
                article['content'] = getFullArticleContent(url = article['url'], pre_content = article['content'], proxies=proxies)
                if not article['content'] == '':
                    output_obj.append(article)
                    titles.append(article['title'])
    if len(titles) == 0:
        news = newsapi.get_everything(q=(company).strip(), language='en')
        for article in news['articles']:
            if article['title'] not in titles:
                del article['source'], article['author'], article['urlToImage']
                article['content'] = getFullArticleContent(url = article['url'], pre_content = article['content'], proxies=proxies)
                if not article['content'] == '':
                    output_obj.append(article)
                titles.append(article['title'])
    return titles, output_obj

def clean_text(text):
    

    #Clean the html tags 
    text = HTMLParser().unescape(text)
    # remove hyperlinks
    text = re.sub(r'https?:\/\/.\S+', "", text)
     
    # remove hashtags
    # only removing the hash # sign from the word
    text = re.sub(r'#', '', text)
     
    # remove old style retweet text "RT"
    text = re.sub(r'^RT[\s]+', '', text)
    
    #One letter in a word should not be present more than twice in continuation
    text = ''.join(''.join(s)[:2] for _, s in itertools.groupby(text))
     
    return text
    
def remove_tags(text):
    return ''.join(xml.etree.ElementTree.fromstring(text).itertext())
def getFullArticleContent(url, pre_content='', proxies=''):
    if not pre_content:
        pre_content=''
    content = ''
    try:
        response = requests.get(url, proxies=proxies)
    except Exception:
        print('Website not reachable')
        return pre_content
    if response.status_code == 200:
        body = response.content
        soup1 = BeautifulSoup(body, 'html.parser')
        # Get all the script type contents from the html code of the article main page (This is the design for EconomicTimes)
        news = soup1.find_all('script')
        
        for article in news:
            try:
                if article.has_attr('type'):
                    # The article is stored in json format
                    if 'json' in article['type']:
                        obj = json.loads(article.contents[0])
                        #NewsArticle is the @type key's value in the json
                        if '@type' in obj.keys():
                            if obj['@type'] ==  'NewsArticle':
                                # articleBody is the key for the article in the json
                                content+=' '+ str(obj["articleBody"])
            except Exception:
                pass
        # This is for the format how US blogs write their articles in div class
        news_div = soup1.find_all('div', class_='article-text')
        for article in news_div:
            try:
                #removing all html tags from the content
                content+=' '+ str(remove_tags(str(article)))
            except Exception:
                pass
        
        # This is for the format how US blogs write their articles in div class
        news_div = soup1.find_all('div', class_='article-content')
        for article in news_div:
            try:
                paragraphs = article.find_all('p')
                for para in paragraphs:
                #removing all html tags from the content
                    content+=' '+ str(remove_tags(str(para)))
            except Exception:
                pass
        
        # This is for the format how US blogs write their articles in div class
        news_div = soup1.find_all('div', class_='entry-content clearfix')
        for article in news_div:
            try:
                paragraphs = article.find_all('p')
                for para in paragraphs:
                #removing all html tags from the content
                    content+=' '+ str(remove_tags(str(para)))
            except Exception:
                pass
        
        if len(content) == 0 or len(content) < len(pre_content):
            content = pre_content.split('… [')[0]
    return clean_text(content)

if __name__=='__main__':
    titles, news = getNews(company='Tesla')
    titles, news = getNews(company='Adani Wilmar')

