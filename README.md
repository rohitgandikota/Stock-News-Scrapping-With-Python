# Stock-News-Scrapping-With-Python

NewsAPI is python library that extracts news from various articles. Although, it restricts the full content of article by 200 chars. So this project aims to extract the full content from html requests manually.  

We also use newspaper library to help extract content after our manual extraction attempt. 

To use the code as it is, please generate a newsapi apikey using the [*link*](https://newsapi.org/register)

Use a summarization and sentiment classification link from your end or opensource. The one we gave in the code is our aws hosted service, to avoid costs, we have masked it in the code provided. 

```
# This function extracts news about Test company's stock news, market sentiment, performance, investor news. 
headlines, news = getNews(company='Tesla')
```
