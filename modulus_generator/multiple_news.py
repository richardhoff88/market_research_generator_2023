import newspaper
from newspaper import Article
from newspaper import Source
from newspaper import news_pool
import pandas as pd
import time

def scrape_articles():
    jec_link = "https://www.jeccomposites.com/"
    print_link = 'https://3dprint.com/'
    electrek_link = "https://electrek.co/"
    printing = newspaper.build(print_link, memoize_articles=False)
    jec_comp = newspaper.build(jec_link, memoize_articles=False)
    electrek = newspaper.build(electrek_link, memoize_articles=False)


    papers = [printing, jec_comp, electrek]

    news_pool.set(papers, threads_per_source=3)
    news_pool.join()

    # Initialize list to collect article data
    articles_data = []

    limit = 3

    for source in papers:

        count = 0
        for article_extract in source.articles:
            if count >= limit:  # Corrected the limit condition
                break

            article_extract.parse()
            if jec_link not in article_extract.url:
                para_list = article_extract.text.split('\n\n')
                para_combined = para_list[0] + "\n" + "\n" + para_list[1]
            else:
                para_list = article_extract.text.split('\n\n')
                para_combined = para_list[1] + "\n" + "\n" + para_list[2]

            paragraph = para_combined + "\n" + "\n" + "Read more: " + article_extract.url
            # Collect article data
            articles_data.append({
                'Title': article_extract.title,
                'Text': paragraph,
                'Source': article_extract.source_url
            })

            count += 1
    return articles_data

def append_to_csv(new_data, filename='article_database.csv'):
    try:
        existing_df = pd.read_csv(filename)
    except FileNotFoundError:
        existing_df = pd.DataFrame(columns=['Title', 'Text', 'Source'])

    new_df = pd.DataFrame(new_data)
    updated_df = pd.concat([existing_df, new_df]).drop_duplicates(subset=['Title']).reset_index(drop=True)
    updated_df.to_csv(filename, index=False)

while True:
    new_articles = scrape_articles()
    append_to_csv(new_articles)
    print("Scraped and appended new articles. Waiting for next round...")
    time.sleep(43200)  # Wait for 12 hours (43200 seconds) before scraping again


