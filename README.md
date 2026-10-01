🎬 Movie Recommendation System

Discover movies you'll love with content-based recommendations.

A Machine Learning-based Movie Recommendation System built using Python, NLP, Scikit-learn, and Streamlit. The system recommends the Top 10 movies similar to a selected movie using TF-IDF Vectorization and Cosine Similarity.

Movie posters are dynamically fetched using the TMDB API, providing an interactive and visual recommendation experience.

✨ Features

🎬 Select a movie from the available movie database

🤖 Get Top 10 similar movie recommendations

🧠 TF-IDF Vectorization for feature representation

📐 Cosine Similarity for measuring movie similarity

🖼️ Fetch movie posters using the TMDB API

🌐 Interactive Streamlit Web Application

⚡ Pre-computed similarity matrix for faster recommendations

📊 Data preprocessing and feature engineering using Python

📌 Overview

With thousands of movies available across different platforms, finding a movie similar to something you already enjoyed can be difficult.

This project uses a content-based recommendation pipeline:

Select a Movie
      ↓
Analyze Movie Features
      ↓
TF-IDF Vectorization
      ↓
Calculate Cosine Similarity
      ↓
Find Similar Movies
      ↓
Top 10 Recommendations
      ↓
Display Movie Posters

The system compares the characteristics and textual features of movies rather than relying on user ratings or other users' preferences.

🧠 Recommendation System

Content-Based Filtering

The project uses a content-based recommendation approach.

The system compares movie features and recommends movies that have similar characteristics to the movie selected by the user.

Recommendation Pipeline

Movie Dataset
      ↓
Data Preprocessing
      ↓
Feature Engineering
      ↓
TF-IDF Vectorization
      ↓
Cosine Similarity
      ↓
Top 10 Similar Movies
      ↓
TMDB Poster Retrieval
      ↓
Streamlit Interface

🔬 How It Works

1. Data Preprocessing

The movie dataset is processed to prepare the required movie information for the recommendation system.

Relevant movie features are combined and transformed into a suitable format for machine learning.

2. TF-IDF Vectorization

TF-IDF (Term Frequency–Inverse Document Frequency) converts textual movie information into numerical vectors.

These vectors represent the movie features mathematically.

3. Cosine Similarity

Cosine Similarity is used to measure the similarity between movie vectors.

A higher similarity score indicates that two movies have more similar feature representations.

4. Recommendation Generation

After calculating similarity scores, movies are sorted based on their similarity to the selected movie.

The system then returns the Top 10 most similar movies.

5. Poster Retrieval

The TMDB API is used to retrieve the poster of each recommended movie.

📸 Application Preview

<p align="center">
  <img src="assets/demo.png" alt="Movie Recommendation System - Streamlit UI" width="900">
</p>

The application provides a clean and interactive interface where users can select a movie and receive the Top 10 similar movie recommendations with movie posters fetched through the TMDB API.

🛠️ Tech Stack

Technology

Purpose

🐍 Python

Core programming language

🐼 Pandas

Data manipulation and preprocessing

🔢 NumPy

Numerical operations

🤖 Scikit-learn

TF-IDF and Cosine Similarity

🌐 Streamlit

Interactive web application

🔗 Requests

API requests

📓 Jupyter Notebook

Data processing and model development

🎬 TMDB API

Movie poster retrieval

🐙 Git & GitHub

Version control

📊 Dataset

This project uses the TMDB 5000 Movie Dataset.

The dataset contains movie-related information including:

Movie titles

Movie IDs

Genres

Keywords

Cast

Crew

Overview

Other movie metadata

Dataset Source

TMDB 5000 Movie Dataset — Kaggle

📁 Project Structure

Movie-Recommendation-System/
│
├── assets/
│   └── demo.png
│
├── app.py
├── Movie_Recommendation_System.ipynb
├── tmdb_5000_movies.csv
├── tmdb_5000_credits.csv
├── requirements.txt
├── .gitignore
└── README.md

Generated Model File

The Jupyter Notebook generates:

movies.pkl

This file contains the processed movie data and cosine similarity matrix required by the Streamlit application.

movies.pkl is excluded from GitHub because of its large file size.

🚀 Installation & Setup

Prerequisites

Make sure you have:

Python 3.x

pip

Git

TMDB API key

1. Clone the Repository

git clone https://github.com/ayush-kumar06/Movie-Recommendation-System.git

2. Navigate to the Project

cd Movie-Recommendation-System

3. Install Dependencies

pip install -r requirements.txt

4. Generate the Model File

Open:

Movie_Recommendation_System.ipynb

Run the required preprocessing and model-building cells.

This will generate:

movies.pkl

Place movies.pkl in the project root directory.

🔐 TMDB API Configuration

This project uses the TMDB API to retrieve movie posters.

For security, your API key should never be uploaded to GitHub.

Create:

.streamlit/secrets.toml

Add:

TMDB_API_KEY = "YOUR_TMDB_API_KEY"

Then access it in app.py:

api_key = st.secrets["TMDB_API_KEY"]

Make sure .streamlit/ is included in .gitignore.

⚠️ Never expose your actual TMDB API key in source code or public repositories.

▶️ Run the Application

Start the Streamlit application:

streamlit run app.py

Streamlit will provide a local URL in the terminal.

Usually:

http://localhost:8501

Open the URL in your browser.

🎯 How to Use

Launch the Streamlit application.

Select a movie from the movie selection dropdown.

Click the Recommend button.

Explore the Top 10 similar movies along with their posters.

📈 Example Workflow

User selects a movie
        ↓
Movie information is processed
        ↓
Text converted using TF-IDF
        ↓
Cosine similarity calculated
        ↓
Movies ranked by similarity
        ↓
Top 10 movies selected
        ↓
TMDB posters fetched
        ↓
Recommendations displayed

📚 Core Concepts

This project demonstrates practical implementation of:

Machine Learning

Natural Language Processing

Content-Based Recommendation

Data Preprocessing

Feature Engineering

TF-IDF

Cosine Similarity

API Integration

Python

Streamlit

👨‍💻 Author

Ayush Kumar

B.Tech — Computer Science & Engineering (AI & ML)

🔗 GitHub: @ayush-kumar06

💼 LinkedIn: Ayush Kumar

🙏 Acknowledgements

TMDB — Movie information and poster API

Kaggle — Movie dataset

Scikit-learn — Machine learning utilities

Streamlit — Web application framework

⭐ Support

If you found this project useful, consider giving the repository a ⭐.

Built with 🐍 Python • 🤖 Machine Learning • 🎬 TMDB • 🌐 Streamlit
