import streamlit as st
import requests
import os

# API key — load from Streamlit Secrets
API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")

def search_similar_books(book_title):
    # Build search URL
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": f"{book_title}",
        "maxResults": 5,
        "key": API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        books = data.get("items", [])

        if not books:
            return None

        # Pick a different book than what user entered
        for book in books:
            info = book["volumeInfo"]
            title = info.get("title", "").lower()
            if book_title.lower() not in title:
                return info  # Found something different

        return books[0]["volumeInfo"]  # Fallback: first result
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Streamlit UI
st.title("📚 Book Recommender")
st.write("Enter a book you like. We'll suggest a similar one!")

book_input = st.text_input("Enter a book title:")

if st.button("Recommend"):
    if not book_input.strip():
        st.warning("Please enter a book title.")
    else:
        with st.spinner("Searching..."):
            rec = search_similar_books(book_input.strip())
            if rec:
                st.subheader(rec.get("title", "Unknown Title"))
                authors = rec.get("authors", ["Unknown Author"])
                st.write(f"**Author:** {', '.join(authors)}")
                st.write(rec.get("description", "No description available."))
                if "imageLinks" in rec:
                    st.image(rec["imageLinks"].get("thumbnail"))
                if "infoLink" in rec:
                    st.markdown(f"[More info →]({rec['infoLink']})")
            else:
                st.error("Couldn't find a similar book. Try another one.")
