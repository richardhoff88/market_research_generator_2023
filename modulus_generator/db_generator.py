import newspaper
from newspaper import news_pool
import sqlite3

def init_db():
    conn = sqlite3.connect('modulus_articles.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS articles
                 (title TEXT PRIMARY KEY,
                   image TEXT, 
                  text TEXT, 
                  source TEXT,
                  is_deleted INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

def insert_article(title, image, text, source):
    conn = sqlite3.connect('modulus_articles.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO articles (title, image, text, source) VALUES (?, ?, ?, ?)", (title, image, text, source))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Article '{title}' already exists in the database.")
    finally:
        conn.close()

def remove_article(title):
    conn = sqlite3.connect('modulus_articles.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE articles SET is_deleted = 1 WHERE title = ?", (title,))
    conn.commit()
    conn.close()

def scrape_articles():
    jec_link = "https://www.jeccomposites.com/"
    print_link = 'https://3dprint.com/'
    electrek_link = "https://electrek.co/"
    weekly_link = "https://compositesweekly.com/"

    printing = newspaper.build(print_link, memoize_articles=False)
    jec_comp = newspaper.build(jec_link, memoize_articles=False)
    electrek = newspaper.build(electrek_link, memoize_articles=False)
    comp_weekly = newspaper.build(weekly_link, memoize_articles=False)

    papers = [printing, jec_comp, electrek, comp_weekly]
    news_pool.set(papers, threads_per_source=3)
    news_pool.join()

    for source in papers:
        if weekly_link not in source.url:
            for article_extract in source.articles[:3]:  # Limit to 3 articles per source
                article_extract.parse()
                image_url = article_extract.top_image
                if jec_link not in article_extract.url:
                    para_list = article_extract.text.split('\n\n')
                    para_combined = para_list[0] + "\n\n" + para_list[1] + "\n\n" + "Read more: " + article_extract.url
                else:
                    para_list = article_extract.text.split('\n\n')
                    para_combined = para_list[1] + "\n\n" + para_list[2] + "\n\n" + "Read more: " + article_extract.url
                insert_article(article_extract.title, image_url, para_combined, article_extract.source_url)
        else:
            for article_extract in source.articles[:1]:  # Limit to 1 article for comp_weekly
                article_extract.parse()
                image_url = article_extract.top_image
                para_list = article_extract.text.split('\n\n')
                para_combined = para_list[0] + "\n\n" + para_list[1] + "\n\n" + "Read more: " + article_extract.url
                insert_article(article_extract.title, image_url, para_combined, article_extract.source_url)

if __name__ == "__main__":
    init_db()  # Initialize the database
    scrape_articles()  # Scrape articles and insert into the database
