import streamlit as st
import pandas as pd
import json
import os
import datetime 
import time
import random
import plotly.express as px
import plotly.graph_objects as go
import requests


#set page configuration


st.set_page_config(
    page_title="Personal Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

#custom css = for styling
st. markdown(""""
<style>)
       .main_header{
             fornt-size: 3rem ! important;
             color:#FF4B4B!important;
             text-align: center !importamt;
             text-shadow2px 2px 4px raba(0,0,0,0,1);

              
             
     }
        .sub_header2{
             fornt-size:2rem ! important;
             color:#FF4B4B! important;
             margin-top:1rem;
             margin-bottom:irem;
             font-weight:bold;

             }
             .success-message{
             padding : 1rem;
             background-color : #ECEFDF5;
             border-radius: 0.375rem;
             border-left 0.375rem;
             boder-color:#382F64;

             } 
             .warning-message{
              padding : 1rem;
             background-color : #ECEFDF5;
              border-radius: 5px solid #F59E0B;
              border-left 0.375rem;
             
             }
             .book-card{
                background-color: #F3F4F6;
                border-radius: 0.5rem;
                padding:1rem;
                boerder: left:5px solid  #3B82F6;
                transition: all 0.3s ease;
             
             }

             .book-card-hover{
                transform: translateY(-5);
                box-shadow: 0 10px 15px  3px rgba(0, 0, 0, 0.1);
             }

             .read-badge{
                background-color: #10B981;
                color: white;
                padding: 0.25rem 0.875rem;
                border-radius: 1rem;
                font-size: 0.75rem;
                font-weight: bold;
                fornt-size: 0.875rem;
                 fonrt-weight: bold;
             }
             .action-button{
              margin-right: 0.5rem;
             
             }
             .stButton{
             border-radius: 0.375rem;
             }
             <style/>

    """,unsafe_allow_html=True)

import requests  # make sure you imported this

def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None


if 'library' not in st.session_state:
    st.session_state.library = []
    if 'search-result'not in st.session_state:
        st.session_state.search_result = []
    if 'book-added' not in st.session_state:
        st.session_state.book_added = False
    if 'book-updated' not in st.session_state:
        st.session_state.book_updated = False
    if'current-book' not in st.session_state:
        st.session_state.current_book = "library"
    
      # Load library from JSON file 
def load_library():
    try:
        if os.path.exists('library.json'):
            with open('library.json', 'r') as file:
                st.session_state.library = json.load(file)
                return True
            return False
                
    except Exception as e:
        st.error(f"Error loading library: {e}")
        return False
    # Save library to JSON file

def save_library():
    try:
        with open('library.json', 'w') as file:
            json.dump(st.session_state.library, file)
            return True
    except Exception as e:
        st.error(f"Error saving library: {e}")
        return False
    
    # add abook to library

def add_book(title, author, genre, status , read,published_date):
    if not title or not author or not genre:
        st.warning("Please fill in all fields")
        return
    book = {
        'title': title,
        'author': author,
        'genre': genre,
        'status': status,
         'read_status': status,  
         'published_date':2022-4-10, 
        'added_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
}
    
    st.session_state.library.append(book)
    save_library()
    st.session_state.book_added = True
    time.sleep(0.10)#animation delay
    #remove books
    def remove_book(index):
        if 0 <= index < len(st.session_state.library):
        
           del st.session_state.library[index]
    save_library()
    st.session_state.book_removed = True
    return True
    return False

    #search_book

def search_books(search_term , search_by):
    search_term = search_term.lower()
    results =[]
    for book in st.session_state.library:
        if search_by == "title" and search_term in book['title'].lower():
            results.append(book)
        elif search_by == "author" and search_term in book['author'].lower():
            results.append(book)
        elif search_by == "genre" and search_term in book['genre'].lower():
            results.append(book)
        elif search_by == "status" and search_term in book['status'].lower():
            results.append(book)
            st.session_state.search_result = results

            #claculate library stats
def get_library_stats():
        total_books = len(st.session_state.library)
        read_books = sum(1 for book in st.session_state.library if book['read_status'])
        percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0

        generes = {}
        authors = {}
        decades = {}

        for book in st.session_state.library:
            if 'genre' in book and 'author' in book:
                if book ['genre'] in generes:
                    generes[book['genre']] += 1
                else:
                    generes[book['genre']] = 1
    #count author
    
            if book['author'] in authors:
                authors[book['author']] += 1
            else:
                authors[book['author']] = 1
    #count decades
        decade = (book['publication_year'] // 10) * 10
        if decade in decades:
            decades[decade] += 1
        else:
            decades[decades] = 1
    #sort by count.
        generes = dict(sorted(generes.items(), key=lambda x : x [1], reverse=True))
        authors = dict(sorted(authors.items(), key=lambda x: x[1], reverse=True))
        decades = dict(sorted(decades.items(), key=lambda x: x [0]))
        return{
            'total_books': total_books,
            'read_books': read_books,
            'percentage_read': percentage_read,
            'generes': generes,
            'authors': authors,
            'decades': decades
        }
        def creat_visulations(status):
            if stats ['total_books'] > 0:
                fig_read_status = go.Figure(data = [go.pie(labels = ['Read', 'Unread Books'],)])
                lable=['Read', 'Unread Books'],
                values = [stats['read_books'], stats['total_books'] - stats['read_books']],
                hole==4
                textinfo='percent+label',
                marker_colors=['#10B981','#F87171']
                fig_redstatus.updata_layout(
                    title_text="Read Vs Unread Books",
                    showlegend=True,
                    height=400,
                )
                st.plotly_chart(fig_read_status, use_container_width=True)
               
                #bar chart for genres
                if stats['genres']:
                    genres_df =pd.dataFrame({
                        'Genre' : list(stats['genres'].keys()),
                        'Count': list(stats['genres'].values())

                    })
                    fig_genres = px.bar(
                        genres_df,
                        x='Genre',
                        y='Count',
                        color='Count',
                        color_continuous_scale=px.colors.sequential.Blues,

                    )

                    fig_genres.update_layout(
                        title_text="Books by bublication decade",
                        xaxis_title="Decade",
                        yaxis_title="Number of Books",
                        height=400,
                    )
                    st.ploty_chart(
                  fig_genres,use_container_width=True)
                          
                    if stats['decsde']:
                        decades_df = pd.DataFrame({
                            'Decade': list(stats['decades'].keys()),
                            'Count': list(stats['decades'].values())
                        })
                        fig_decades = px.bar(
                            decades_df,
                            x='Decade',
                            y='Count',
                            markers =true,
                            line_sape ='Spline',
                        )
                        fig_decades.update_layout(
                            title_text="Books by bublication decade",
                            xaxis_title="Decade",
                            yaxis_title="Number of Books",
                            height=400,
                        )
                        st.plotly_chart(fig_decades, use_container_width=True)
                        #load library
        def load_library():
            st.sidebar.markdown("<h1 style='text-align: center;'>Library Managetion </h1>", unsafe_allow_html=True)
            lottie_book = load_lottieurl("https://assets9.lottiefiles.com/temp/lf20_aKAfIn.json")
            if lottie_book:
                st_lottie(lottie_book, speed=1, width=300, height=200, key="book")

                nav_options = s.t.sidebar.radio(
                    "choose an option:",
                    ["View Library", "Add Book", "Search Book", "Library Statics"],


                )
                if nav_options == "View Library":
                
                   st. session_state.Current_view ='library'
            elif nav_options == "Add Book":
                       st.session_state.current_view = 'add_book'
            elif nav_options == "Search Book":
                       st.session_state.current_view = 'search_book'
            elif nav_options == "Library Statics":
                       st.session_state.current_view = 'library_statistics'
            else:
                       st.session_state.current_view = 'stats'
                       st.markedown("<h1 class='main_header'>Personal library Management System</h1>", unsafe_allow_html=True)
                       if st. session_state.current_view == 'add':
                            st.markdown("<h2 class='sub_header'>Add Book</h2>", unsafe_allow_html=True)
                        
                #adding books input from.
                       
        st.form(key='add_book_form')
        col1,col2 = st.columns(2)
        with col1:
            title = st.text_input("Book Title", max_chars =100)
            author = st.text_input("Author", max_chars=100)
            published_year = st.text_input("Published Year", min_value=1000, max_value = datetime.now().year,step=1,value=2023)
            
            with col2:
                genre =st.selectbox("Genre",[
                    "Fiction", "Non-Fiction", "Science", "History", "Biography","Religions","Love poetry","Sad poetry","Self help","Technalogy","Romance","Art","Gernal knowledge","Holy Books","Islamic Hadees","Cosmplogy","Others categories,"]
                    )
            read_status = st.selectbox("Read Status",["Read","Unread"])
            read_bool = read_status == "Read"
            submit_button = st.from_button("lable = Add Book", key="add_book")
            
            if submit_button and title and author and genre:
              add_book(title, author, genre, read_bool, published_year)
            st.success("Book added successfully!")
   
            if st.session_state.book_added:
                 st.markdown("<div class='success-message'>Book added successfully!</div>", unsafe_allow_html=True)
                 st.baloons()
                 st.sessions_state_added = False

            elif st.session_state.Current_view == "library":
                 st.markdown("<h2 class='sub_header'>Library</h2>", unsafe_allow_html=True)
                 st.session_state.library = load_library()
                 if not st.session_state.library:
                     st.markdown("<div class='warning-message'>No books found in the library.</div>", unsafe_allow_html=True)
                     st.warning("No books found in the library.")
                 else:
                      clls = st. columns(2)
                      for i , book in enumerate(st.session_state.library):
                          with cols[i % 2]:
                              st.markdown(f"""<div class='book-card'> 
                             <h3>{book['title']}</h3>
                             <p><strong>Author:</strong> {book['author']}</p>
                             <p><strong>Genre:</strong> {book['genre']}</p>
                            <p><strong>Read Status:</strong> {book['read_status']}</p>
                             <p><strong>Published Year:</strong> {book['published_year']}</p>
                              <><  class= '{read_badge if book[read_status] else "unread-badge"}'>{
                                          "Read" if book["read_status"] else "Unread"}</span></p>           
                                          """, unsafe_allow_html=True)
                              col1,col2 = st.columns(2)
                              with col1:
                                  if st.button("Remove Book", key=f"remove_{i}", use_container_width=True):
                                   if   remove_book(i):
                                       with col2: 
                                         new_status = not book['read_status']
                                         status_lable = "Markt as read " if not book['read status'] else "Markt Unread"
                                         if st.button(status_lable,key=f"status_{i}", use_container_width=True):
                                             st.sessions_state.library[i]['read_status'] = new_status
                                             save_library()
                                             st.rerun()
                                   if         st.session_state.book_removed:
                                           st.markdown("<div class='success-message'>Book removed successfully!</div>", unsafe_allow_html=True)
                                           st.session_state.book_removed = False
                                   elif      st.session_state.current_view == "search_book":
                                       st.markdown("<h2 class='sub_header'>Search Book</h2>", unsafe_allow_html=True)
                                       search_by == st.selectbox("Search By", ["Title", "Author", "Genre"])
                                       search_term = st.text_input("Enter Search Term:")
                                  if    st.button("Search",use_container_width=False):
                                      if search_trem:
                                          with st.spinner("searching..."):
                                                time.sleep(0.5)
                                                search_books(search_term, search_by)
                                                if hasatter(st.session_state, 'search_result') :
                                                     
                                                     if st.session_state.search_result:
                                                        for i, book in st.session_state.search_result:
                                                            st.markdown(f"""<div class='book-card'>
                                                            <h3>{book['title']}</h3>
                                                            <p><strong>Author:</strong> {book['author']}</p>
                                                            <p><strong>Genre:</strong> {book['genre']}</p>
                                                            <p><strong>Read Status:</strong> {book['read_status']}</p>
                                                            <p><strong>Published Year:</strong> {book['published_year']}</p>
                                                            </div>""", unsafe_allow_html=True)
                                                     elif search_term:
                                                         st.markdown("<div class='warning-message'>No books found.</div>", unsafe_allow_html=True)
                                                         st.warning("No books found.")
                                                     elif st.session_state.current_view == "stats":
                                                            st.markdown("<h2 class='sub_header'>Library Statistics</h2>", unsafe_allow_html=True)
                                                if not st.session_state.library:
                                                     st.markdown("<div class='warning-message'>No books found in the library.</div>", unsafe_allow_html=True)
                                                else:
                                                     stats = get_library_stats() 
                                                     col1,col2,col3 = st.columns(3) 
                                                     with col1:
                                                            st.metric("Total Books", stats['total_books'])  
                                                            with col2:
                                                                st.metric("Read Books", stats['read_books'])
                                                                with col3:
                                                                    st.metric("Percentage Read", f"{stats['percentage_read']:.1f}%")
                                                                    if stats['total_books'] > 0:
                                                                        create_visualizations()
                                                                    if stats ['outher']:
                                                                        st.markdown("<h3 class='sub_header'>Books by Author</h3>", unsafe_allow_html=True)
                                                                        top_authors = dict(list (stats['authors'].items())[:5])
                                                                    for author, count in top_authors.items():
                                                                        st.markdown(f"**{author}**: {count}books{'s' if count > 1 else ''}")
                                                                        st.markdown("---")
                                                                        st.markdown("Copyright @ 2025,Ghousia Maqsood,personal library management system, all rights reserved",unsafe_allow_html = True)
                                                                    

                                                                         
