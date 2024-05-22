import streamlit as st
import requests
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import streamlit as st
import os


st.set_page_config(
        page_title="Stock X",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
)


with open(os.path.join('pages', 'styles2.css')) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True) 



urls = ["https://www.moneycontrol.com/news/tags/companies.html", "https://www.moneycontrol.com/news/business.html"]

scraped_articles = []

def reduce_paragraph(paragraph, num_sentences=2):
    """Reduces a paragraph to a specified number of sentences using LexRank summarization."""
    parser = PlaintextParser.from_string(paragraph, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    summary = summarizer(parser.document, num_sentences)
    reduced_paragraph = ' '.join(str(sentence) for sentence in summary)
    return reduced_paragraph


@st.cache_resource
def fetch_url_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve the webpage {url}. Status code:", response.status_code)
        return None

@st.cache_resource
def fetch_article_data(url):
    html_doc = fetch_url_content(url)
    if html_doc is None:
        return None

    temp = BeautifulSoup(html_doc, 'html.parser')
    target_script = temp.find_all('script', type='application/ld+json')
    if len(target_script) > 2:
        target = target_script[2]
        script_content = target.string.strip()
        articleBody = script_content[(script_content.find('articleBody') + 13):(script_content.find('"author"')):]
        word_count = len(articleBody.split())
        if word_count > 200:
            articleBody = reduce_paragraph(articleBody)
        new_body = ' '.join(articleBody.split()[:200])  # Limit to 200 words

        return {
            "article_body": new_body,
            "word_count": len(new_body.split())
        }
    else:
        print("Failed to find required data in script tag. Skipping this article.")
        return None

# ...

for url in urls:
    response_text = fetch_url_content(url)
    if response_text is None:
        continue

    soup = BeautifulSoup(response_text, 'html.parser')
    news_items = soup.find_all('li', class_='clearfix')

    for item in news_items:
        if item.find(class_='isPremiumCrown'):
            continue

        try:
            title = item.find('h2').text
            content = item.find('p').text
            href_content = item.find('a')['href']
            date = item.find('span').text

            article_data = fetch_article_data(href_content)
            if article_data is None:
                continue

            article_data.update({
                "title": title,
                "content": content,
                "href_content": href_content,
                "date": date,
            })

            scraped_articles.append(article_data)
        except Exception as e:
            st.error("Error occurred while processing an article:" + str(e))

# ...
st.markdown("<h1 class='Title' >News Aticles</h1>", unsafe_allow_html=True)

for article in scraped_articles:
    st.header(article['title'])
    st.write(f"Date: {article['date']}")
    st.write(article['content'])
    st.write(f"Summary: {article['article_body']}")
    st.write("---")  # Separator between articles