import requests
import psycopg2

# Database config (edit if needed)
conn = psycopg2.connect(
    dbname="postdb",
    user="postgres",
    password="secret",
    host="localhost",
    port=5432
)
cur = conn.cursor()

# Fetch posts from mock API
resp = requests.get("https://jsonplaceholder.typicode.com/posts")
posts = resp.json()

# Insert each post into the database
for post in posts:
    cur.execute("""
        INSERT INTO posts (id, userId, title, body)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
    """, (post["id"], post["userId"], post["title"], post["body"]))

conn.commit()
cur.close()
conn.close()
print("Database populated from API!")
