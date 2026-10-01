import html
import pickle

import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inline SVG shown when a poster cannot be loaded (no external file needed)
PLACEHOLDER_POSTER = (
    "data:image/svg+xml;utf8,"
    "<svg xmlns='http://www.w3.org/2000/svg' width='500' height='750' viewBox='0 0 500 750'>"
    "<rect width='500' height='750' fill='%23191d27'/>"
    "<text x='250' y='350' font-size='90' text-anchor='middle'>🎬</text>"
    "<text x='250' y='430' font-family='sans-serif' font-size='26' "
    "text-anchor='middle' fill='%238a91a3'>Poster unavailable</text>"
    "</svg>"
)


# =============================================================================
# LOAD DATA  (unchanged)
# =============================================================================
# Load the processed data and similarity matrix
with open('movies.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)


# =============================================================================
# RECOMMENDATION FUNCTIONS  (unchanged)
# =============================================================================
# Function to get movie recommendations
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Get top 10 similar movies
    movie_indices = [i[0] for i in sim_scores]
    return movies[['title', 'movie_id']].iloc[movie_indices]


# =============================================================================
# TMDB FUNCTIONS
# =============================================================================
# Fetch movie poster from TMDB API  (original function, unchanged)
def fetch_poster(movie_id):
    api_key = '7b995d3c6fd91a2284b4ad8cb390c7b8'  # Replace with your TMDB API key
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
    return full_path


@st.cache_data(show_spinner=False)
def _cached_poster(movie_id):
    """Cache successful lookups so repeat searches are instant.
    Raises on failure, and Streamlit never caches exceptions, so a temporary
    network error will be retried on the next run."""
    url = fetch_poster(movie_id)
    # TMDB returns poster_path = null for some movies -> URL ends with "None"
    if url.endswith("None"):
        raise ValueError("No poster available for this movie")
    return url


def fetch_poster_safe(movie_id):
    """Wrapper around fetch_poster(). Never raises.
    Returns (poster_url, ok). On failure returns the placeholder and ok=False."""
    try:
        return _cached_poster(int(movie_id)), True
    except Exception:
        return PLACEHOLDER_POSTER, False


# =============================================================================
# CUSTOM CSS
# =============================================================================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&family=DM+Sans:wght@400;500;600&display=swap');

:root {
  --bg: #0b0e14;
  --surface: #151a24;
  --surface-2: #1c2230;
  --line: rgba(255,255,255,0.08);
  --text: #f3f4f7;
  --muted: #9aa2b4;
  --accent: #f5b740;
  --accent-2: #e5484d;
}

/* ---------- Base app ---------- */
.stApp {
  background:
    radial-gradient(1100px 500px at 15% -10%, rgba(229,72,77,0.16), transparent 60%),
    radial-gradient(900px 500px at 95% 0%, rgba(245,183,64,0.10), transparent 55%),
    var(--bg);
  color: var(--text);
  font-family: 'DM Sans', sans-serif;
}
.block-container { max-width: 1240px; padding-top: 2rem; padding-bottom: 3rem; }

/* Hide Streamlit chrome but keep the sidebar toggle usable */
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }

/* ---------- Hero ---------- */
.hero {
  padding: 3.2rem 2.5rem;
  border-radius: 24px;
  border: 1px solid var(--line);
  background:
    linear-gradient(120deg, rgba(229,72,77,0.20), rgba(245,183,64,0.08) 55%, rgba(21,26,36,0.6)),
    var(--surface);
  box-shadow: 0 20px 60px rgba(0,0,0,0.45);
}
.hero-badge {
  display: inline-block;
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--accent);
  background: rgba(245,183,64,0.12);
  border: 1px solid rgba(245,183,64,0.35);
  margin-bottom: 1.1rem;
}
.hero h1 {
  font-family: 'Sora', sans-serif;
  font-weight: 800;
  font-size: clamp(2rem, 4.6vw, 3.4rem);
  line-height: 1.1;
  letter-spacing: -0.02em;
  margin: 0 0 0.8rem 0;
  padding: 0;
  color: var(--text);
}
.hero p { font-size: 1.15rem; color: var(--muted); margin: 0; max-width: 560px; }

/* ---------- Search panel (st.container key="search_panel") ---------- */
.st-key-search_panel {
  margin-top: 1.5rem;
  padding: 1.6rem 1.8rem 1.8rem;
  border-radius: 20px;
  background: var(--surface);
  border: 1px solid var(--line);
  box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}
.panel-label {
  font-family: 'Sora', sans-serif;
  font-weight: 600;
  font-size: 1.05rem;
  color: var(--text);
  margin-bottom: 0.2rem;
}
.panel-hint { color: var(--muted); font-size: 0.92rem; margin-bottom: 0.9rem; }

/* Selectbox */
div[data-baseweb="select"] > div {
  background-color: var(--surface-2) !important;
  border: 1px solid var(--line) !important;
  border-radius: 12px !important;
  min-height: 52px;
  color: var(--text) !important;
}
div[data-baseweb="select"] > div:hover,
div[data-baseweb="select"] > div:focus-within { border-color: var(--accent) !important; }
div[data-baseweb="select"] span, div[data-baseweb="select"] input { color: var(--text) !important; }
ul[role="listbox"] { background: var(--surface-2) !important; }
ul[role="listbox"] li { color: var(--text) !important; }

/* Button */
.stButton > button {
  width: 100%;
  height: 52px;
  border-radius: 12px;
  border: none;
  font-family: 'Sora', sans-serif;
  font-weight: 600;
  font-size: 1rem;
  color: #17120a;
  background: linear-gradient(135deg, #f7c15a, #f5a623);
  box-shadow: 0 6px 18px rgba(245,166,35,0.25);
  transition: transform .18s ease, box-shadow .18s ease, filter .18s ease;
}
.stButton > button:hover {
  transform: translateY(-2px);
  filter: brightness(1.06);
  box-shadow: 0 12px 26px rgba(245,166,35,0.40);
  color: #17120a;
  border: none;
}
.stButton > button:active { transform: translateY(0); }
.stButton > button:focus-visible { outline: 2px solid #fff; outline-offset: 2px; }

/* ---------- Section headings ---------- */
.section-head { margin: 2.6rem 0 1.3rem; }
.section-head h2 {
  font-family: 'Sora', sans-serif;
  font-weight: 700;
  font-size: 1.8rem;
  letter-spacing: -0.01em;
  margin: 0; padding: 0;
  color: var(--text);
}
.section-head p { color: var(--muted); margin: 0.35rem 0 0; font-size: 1rem; }
.section-head b { color: var(--accent); font-weight: 600; }

/* ---------- Movie grid ---------- */
.movie-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 22px;
}
@media (max-width: 1100px) { .movie-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); } }
@media (max-width: 860px)  { .movie-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
@media (max-width: 580px)  { .movie-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; } }

.movie-card {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 14px rgba(0,0,0,0.30);
  transition: transform .25s ease, box-shadow .25s ease, border-color .25s ease;
}
.movie-card:hover {
  transform: translateY(-6px);
  border-color: rgba(245,183,64,0.35);
  box-shadow: 0 18px 40px rgba(0,0,0,0.60);
}
.poster-wrap {
  aspect-ratio: 2 / 3;       /* fixed poster ratio */
  overflow: hidden;
  background: var(--surface-2);
}
.poster-wrap img {
  width: 100%; height: 100%;
  object-fit: cover;         /* fills the frame without distortion */
  display: block;
  transition: transform .4s ease;
}
.movie-card:hover .poster-wrap img { transform: scale(1.06); }
.card-body { padding: 0.8rem 0.9rem 1rem; }
.card-title {
  font-family: 'Sora', sans-serif;
  font-weight: 600;
  font-size: 0.93rem;
  line-height: 1.3;
  color: var(--text);
  min-height: 2.4em;         /* keeps cards aligned for 1-2 line titles */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 0.55rem;
}
.rec-badge {
  display: inline-block;
  font-size: 0.72rem;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 999px;
  color: var(--accent);
  background: rgba(245,183,64,0.12);
  border: 1px solid rgba(245,183,64,0.30);
}

/* ---------- Empty state ---------- */
.empty-state {
  margin-top: 2.4rem;
  text-align: center;
  padding: 3.5rem 1.5rem;
  border: 1px dashed rgba(255,255,255,0.16);
  border-radius: 20px;
  background: rgba(21,26,36,0.55);
}
.empty-icon { font-size: 3rem; margin-bottom: 0.6rem; }
.empty-state h3 {
  font-family: 'Sora', sans-serif;
  font-weight: 700; font-size: 1.5rem;
  margin: 0 0 0.4rem; padding: 0; color: var(--text);
}
.empty-state p { color: var(--muted); margin: 0; font-size: 1rem; }

/* ---------- Footer ---------- */
.app-footer {
  margin-top: 3.5rem;
  padding-top: 1.4rem;
  border-top: 1px solid var(--line);
  text-align: center;
  color: var(--muted);
  font-size: 0.88rem;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] { background: #0f131b; border-right: 1px solid var(--line); }
section[data-testid="stSidebar"] * { color: var(--text); }
section[data-testid="stSidebar"] h3 { font-family: 'Sora', sans-serif; }
.side-muted { color: var(--muted) !important; font-size: 0.92rem; line-height: 1.55; }

/* Respect users who prefer reduced motion */
@media (prefers-reduced-motion: reduce) {
  .movie-card, .poster-wrap img, .stButton > button { transition: none; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# =============================================================================
# SIDEBAR  (optional, minimal)
# =============================================================================
with st.sidebar:
    st.markdown("### 🎬 About")
    st.markdown(
        "<div class='side-muted'>A content-based movie recommender. Pick a movie "
        "and get the 10 most similar titles.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("### How it works")
    st.markdown(
        "<div class='side-muted'>Movie metadata is converted into feature vectors. "
        "Cosine similarity between the vectors ranks every movie against your "
        "selection, and the top 10 matches are shown.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("### Technologies")
    st.markdown(
        "<div class='side-muted'>Python<br>Streamlit<br>Pandas<br>"
        "Cosine Similarity (ML)<br>TMDB API</div>",
        unsafe_allow_html=True,
    )


# =============================================================================
# HEADER
# =============================================================================
st.markdown(
    "<div class='hero'>"
    "<div class='hero-badge'>AI-Powered Recommendation Engine</div>"
    "<h1>🎬 Movie Recommendation System</h1>"
    "<p>Discover movies you'll love based on your taste.</p>"
    "</div>",
    unsafe_allow_html=True,
)


# =============================================================================
# MOVIE SELECTION
# =============================================================================
if "results" not in st.session_state:
    st.session_state.results = None       # (source_title, recommendations)

with st.container(key="search_panel"):
    st.markdown(
        "<div class='panel-label'>Choose a Movie</div>"
        "<div class='panel-hint'>Start typing to search the catalogue.</div>",
        unsafe_allow_html=True,
    )
    col_select, col_button = st.columns([3, 1], vertical_alignment="bottom")
    with col_select:
        selected_movie = st.selectbox(
            "Choose a Movie",
            movies['title'].values,
            label_visibility="collapsed",
        )
    with col_button:
        recommend_clicked = st.button("Recommend Movies")

if recommend_clicked:
    with st.spinner("Finding movies you'll love..."):
        st.session_state.results = (selected_movie, get_recommendations(selected_movie))


# =============================================================================
# RECOMMENDATIONS
# =============================================================================
def build_card(title, poster_url):
    """Return the HTML for a single movie card."""
    return (
        "<div class='movie-card'>"
        f"<div class='poster-wrap'><img src=\"{poster_url}\" alt=\"{html.escape(title)} poster\" "
        "loading='lazy'></div>"
        "<div class='card-body'>"
        f"<div class='card-title' title=\"{html.escape(title)}\">{html.escape(title)}</div>"
        "<span class='rec-badge'>Recommended</span>"
        "</div></div>"
    )


if st.session_state.results is None:
    # Empty state: shown before the first recommendation
    st.markdown(
        "<div class='empty-state'>"
        "<div class='empty-icon'>🍿</div>"
        "<h3>Find your next favorite movie</h3>"
        "<p>Select a movie above and let our recommendation engine do the rest.</p>"
        "</div>",
        unsafe_allow_html=True,
    )
else:
    source_title, recommendations = st.session_state.results

    st.markdown(
        "<div class='section-head'>"
        "<h2>Recommended For You</h2>"
        f"<p>Because you liked <b>{html.escape(source_title)}</b></p>"
        "</div>",
        unsafe_allow_html=True,
    )

    cards, failed = [], 0
    with st.spinner("Loading posters..."):
        for _, row in recommendations.iterrows():
            poster_url, ok = fetch_poster_safe(row['movie_id'])
            failed += 0 if ok else 1
            cards.append(build_card(row['title'], poster_url))

    # One responsive CSS grid: 5 per row on desktop, fewer on smaller screens
    st.markdown("<div class='movie-grid'>" + "".join(cards) + "</div>", unsafe_allow_html=True)

    if failed:
        st.warning(
            f"{failed} poster(s) could not be loaded from TMDB. "
            "Titles are still shown; try again in a moment."
        )


# =============================================================================
# FOOTER
# =============================================================================
st.markdown(
    "<div class='app-footer'>Built with Python • Streamlit • Machine Learning • TMDB</div>",
    unsafe_allow_html=True,
)