import sqlite3
import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize Chroma client
client = chromadb.Client(
    settings=chromadb.config.Settings(
        persist_directory="./chroma_db",
        is_persistent=True
    )
)
collection = client.get_or_create_collection("books")

def build_vector_store():
    from db import get_connection

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT id, title, author, category, description, price, availability
            FROM books
        """)
        rows = cur.fetchall()

    for row in rows:
        book_id, title, author, category, description, price, quantity = row

        combined_text = f"""
        Title: {title}
        Author: {author}
        Category: {category}
        Description: {description}
        """

        embedding = model.encode(combined_text)

        collection.add(
            ids=[str(book_id)],
            embeddings=[embedding],
            metadatas=[{
                "id": book_id,
                "title": title,
                "author": author,
                "price": price,
                "category": category,
                "quantity": quantity
            }]
        )

    conn.close()
    print("✅ Vector store created!")

# Only run if file executed directly
if __name__ == "__main__":
    build_vector_store()