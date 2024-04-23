import os
from db import Database
import streamlit as st
from dotenv import load_dotenv
from db import Database

load_dotenv()

def display_books(books):
    container = st.container()
    bottom_menu = st.columns((4, 2, 1))
    with bottom_menu[2]:
        batch_size = st.selectbox("Page Size", options=[25, 50, 100])
    with bottom_menu[1]:
        total_pages = (
            int(len(books) / batch_size) if int(len(books) / batch_size) > 0 else 1
        )
        current_page = st.number_input(
            "Page", min_value=1, max_value=total_pages, step=1
        )
    with bottom_menu[0]:
        st.markdown(f"Page **{current_page}** of **{total_pages}** ")

    with container:
        books = books[batch_size * (current_page-1) : batch_size * current_page - 1]
        if not books:
            return
        for book in books:
            with st.expander(f'{book[1]} {":star:" * book[2]}'):
                st.markdown(f'''
- Price: {book[3]} pounds 
- {book[4]}
                ''')

st.title('Book shop')
st.subheader('A simple app to webscrap a book website and display all infos')

st.markdown('---')


# Search, sort, and filter bar
search_query = st.text_input("Search books")
sort_column = st.selectbox("Sort by", ["title", "rating", "price"], index=1)
sort_order = st.selectbox("Order by", ["from high to low", "from low to high"], index=0)
filter_in_stock = st.checkbox("Filter In Stock Only")

with Database(os.getenv('DATABASE_URL')) as db:
    books = db.query_table(search_query, sort_column, sort_order, filter_in_stock)
    display_books(books)

# sys.exit()