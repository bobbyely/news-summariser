import requests
from bs4 import BeautifulSoup
import re


def scrape_article(url:  str) -> dict:
    """scrape an abc article for text, title etc.

    Args:
        url (str): url of a abc.net.au/news article

    Returns:
        dict: dictionary of article title, topics, text, url and post date
    """

    # try and get a response
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"},
                           timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')

    except Exception as e:
        print(f"Couldn't scrape soup from url - {e}")

    # try and soup the article
    try:
        # Get the title
        title = soup.find_all('h1')[0].text

        # Get the topics
        topics = soup.find_all('a', class_=re.compile('ArticleHeadlineTitle'))
        topics = [x.text for x in topics]

        # article text
        article_text = soup.find_all('div',
                                     class_=re.compile(
                                         'ArticleRender'))[0].text

        # Clean out the date
        post_date = url.split('/')[4]

        article_dict = {}
        article_dict['title'] = title
        article_dict['topics'] = topics
        article_dict['text'] = article_text
        article_dict['url'] = url
        article_dict['post_date'] = post_date

    except Exception as e:
        print(e)
        article_dict = {}
        article_dict['title'] = ''
        article_dict['topics'] = ''
        article_dict['text'] = ''
        article_dict['url'] = url
        article_dict['post_date'] = ''

    return article_dict


def get_article_urls(top_url) -> list[str]:
    """Given the landing page url (abc.net.au/news#top), provide a list
    of news article urls

    Args:
        top_url (_type_): url of https://www.abc.net.au/news

    Returns:
        list[str]: A list of news article urls
    """
    res = requests.get(top_url, headers={"User-Agent": "Mozilla/5.0"},
                       timeout=10)
    soup = BeautifulSoup(res.text, 'html.parser')

    links = soup.find_all('a', class_=re.compile('GenericCard'))
    links2 = soup.find_all('a',
                           class_=re.compile(r'interactive_focusContext'))[:3]

    links = links + links2

    # grab the actual href
    link_list = []

    for i in range(len(links)):
        try:
            link_list.append(links[i]['href'])
        except Exception as e:
            print(f"Warning: Couldn't get link - {e} for link {links[i]}")

    link_list_final = []

    # mini_dict for numbers (dates) in url
    for link in link_list:
        if any(char.isdigit() for char in link):
            link_list_final.append(link)

    # prepend start url
    start_url = 'https://www.abc.net.au'

    final_list = [f"{start_url}{x}" for x in link_list_final]

    return final_list
