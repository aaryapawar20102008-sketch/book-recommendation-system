import os
import gdown
import streamlit as st
import pickle
import pandas as pd


# ----------------------------
# Page Configuration
# ----------------------------

st.set_page_config(
    page_title="Book Recommendation System",
    page_icon="📚",
    layout="wide"
)

# ----------------------------
# Custom CSS
# ----------------------------

st.markdown("""
<style>

.stApp{
background-color:#FFF8F0;
}

h1{
text-align:center;
color:#4A4A4A;
}

.book-card{
background:white;
padding:20px;
border-radius:15px;
box-shadow:0px 4px 15px rgba(0,0,0,0.15);
margin-bottom:20px;
border-left:8px solid #4F8BF9;
}

.book-title{
font-size:22px;
font-weight:bold;
color:#1E3A5F;
}

.author{
font-size:17px;
color:#555;
}

.publisher{
font-size:15px;
color:#777;
}

.rating{
font-size:18px;
color:#F4B400;
font-weight:bold;
}

div.stButton>button{
background:#4F8BF9;
color:white;
border-radius:10px;
height:50px;
font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# Load Data
# ----------------------------

books = pd.read_csv("cleaned_data.csv", on_bad_lines="skip")
FILE_ID = "1c6CidY2YCP0TeB03_5rW_cmi0T7c_ccY"

if not os.path.exists("similarity.pkl"):
    url = f"https://drive.google.com/uc?id={FILE_ID}"
    gdown.download(url, "similarity.pkl", quiet=False)
similarity = pickle.load(open("similarity.pkl","rb"))

# ----------------------------
# Recommendation Function
# ----------------------------

def recommend(book):

    index = books[books['title']==book].index[0]

    distances = similarity[index]

    books_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x:x[1]
    )[1:6]

    recommendations=[]

    for i in books_list:

        recommendations.append({

            "title":books.iloc[i[0]].title,

            "author":books.iloc[i[0]].authors,

            "publisher":books.iloc[i[0]].publisher,

            "rating":books.iloc[i[0]].average_rating

        })

    return recommendations

# ----------------------------
# Header
# ----------------------------

st.title("📚 Smart Book Recommendation System")


st.divider()

# ----------------------------
# Book Selection
# ----------------------------

selected_book = st.selectbox(

"📖 Select a Book",

books['title'].values

)

# ----------------------------
# Recommend Button
# ----------------------------

if st.button("✨ Recommend Books"):

    recommendations = recommend(selected_book)

    st.subheader("Recommended Books")

    for book in recommendations:

        st.markdown(f"""

<div class="book-card">

<div class="book-title">

📘 {book['title']}

</div>

<br>

<div class="author">

✍ Author : {book['author']}

</div>

<br>

<div class="publisher">

🏢 Publisher : {book['publisher']}

</div>

<br>

<div class="rating">

⭐ Rating : {book['rating']}

</div>

</div>

""",unsafe_allow_html=True)