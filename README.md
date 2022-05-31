# Stock-News-Scrapping-With-Python

NewsAPI is python library that extracts news from various articles. Although, it restricts the full content of article by 200 chars. So this project aims to extract the full content from html requests manually.  

We also use newspaper library to help extract content after our manual extraction attempt. 


```
# This function extracts news about Test company's stock news, market sentiment, performance, investor news. 
headlines, news = getNews(company='Tesla')
```
