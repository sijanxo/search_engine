from wiki import article_metadata, ask_search, ask_advanced_search
import datetime
import time


def keyword_to_titles(metadata):
    keyword_to_titles_dict = {}
    for article in metadata:
        for keyword in article[4]:
            if keyword in keyword_to_titles_dict:
                keyword_to_titles_dict[keyword].append(article[0])
            else:
                keyword_to_titles_dict[keyword] = [article[0]]
    return keyword_to_titles_dict


def title_to_info(metadata):
    title_to_info_dict = {}
    for article in metadata:
        title_to_info_dict[article[0]] = {
            'author': article[1],
            'timestamp': article[2],
            'length': article[3]
        }
    return title_to_info_dict


def search(keyword, keyword_to_titles):
    try:
        titles_with_keyword = keyword_to_titles[keyword]
        return titles_with_keyword
    except KeyError:
        return []

'''
Functions 4-8 are called after searching for a list of articles containing the user's keyword.
'''

def article_length(max_length, article_titles, title_to_info):
    titles_within_count = []
    for article_title in article_titles:
        if title_to_info[article_title]['length'] <= max_length:
            titles_within_count.append(article_title)
    return titles_within_count


def key_by_author(article_titles, title_to_info):
    author_to_article_dict = {}
    for article_title in article_titles:
        author = title_to_info[article_title]['author']
        if author in author_to_article_dict:
            author_to_article_dict[author].append(article_title)
        else:
            author_to_article_dict[author] = [article_title]
    return author_to_article_dict


def filter_to_author(author, article_titles, title_to_info):
    try:
        author_to_article_dict = key_by_author(article_titles, title_to_info)
        from_author = author_to_article_dict[author]
        return from_author
    except KeyError:
        return []

def filter_out(keyword, article_titles, keyword_to_titles):
    try:
        articles_without_keyword = []
        for article_title in article_titles:
            if not article_title in keyword_to_titles[keyword]:
                articles_without_keyword.append(article_title)
        return articles_without_keyword
    except KeyError:
        return []

def articles_from_year(year, article_titles, title_to_info):
    first_day_of_year = datetime.date(year, 1, 1)
    last_day_of_year = datetime.date(year+1, 1, 1) 
    first_day_unix = int(time.mktime(first_day_of_year.timetuple()))
    last_day_unix = int(time.mktime(last_day_of_year.timetuple()))

    articles_from_year_list = []

    for article_title in article_titles:
        if title_to_info[article_title]['timestamp'] in range(first_day_unix, last_day_unix):
            articles_from_year_list.append(article_title)
    
    return articles_from_year_list

# Prints out articles based on searched keyword and advanced options
def display_result():
    # Preprocess all metadata to dictionaries
    keyword_to_titles_dict = keyword_to_titles(article_metadata())
    title_to_info_dict = title_to_info(article_metadata())
    
    # Stores list of articles returned from searching user's keyword
    articles = search(ask_search(), keyword_to_titles_dict)

    # advanced stores user's chosen advanced option (1-7)
    # value stores user's response in being asked the advanced option
    advanced, value = ask_advanced_search()

    if advanced == 1:
        # value stores max length of articles
        # Update articles to contain only ones not exceeding the maximum length
        articles = article_length(value, articles, title_to_info_dict)
    if advanced == 2:
        # Update articles to be a dictionary keyed by author
        articles = key_by_author(articles, title_to_info_dict)
    elif advanced == 3:
        # value stores author name
        # Update article metadata to only contain titles and timestamps
        articles = filter_to_author(value, articles, title_to_info_dict)
    elif advanced == 4:
        # value stores a second keyword
        # Filter articles to exclude those containing the new keyword.
        articles = filter_out(value, articles, keyword_to_titles_dict)
    elif advanced == 5:
        # value stores year as an int
        # Update article metadata to contain only articles from that year
        articles = articles_from_year(value, articles, title_to_info_dict)

    print()

    if not articles:
        print("No articles found")
    else:
        print("Here are your articles: " + str(articles))

if __name__ == "__main__":
    display_result()
    
