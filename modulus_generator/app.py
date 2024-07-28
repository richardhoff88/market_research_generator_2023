from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('modulus_articles.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    articles = conn.execute('SELECT * FROM articles WHERE is_deleted = 0 ORDER BY ROWID DESC').fetchall()
    conn.close()
    return render_template('index.html', articles=articles)

@app.route('/remove_article/<title>')
def remove_article(title):
    conn = get_db_connection()
    conn.execute("UPDATE articles SET is_deleted = 1 WHERE title = ?", (title,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
