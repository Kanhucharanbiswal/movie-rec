import requests
import streamlit as st
from datetime import datetime
import time

# =============================
# CONFIG
# =============================
API_BASE = "https://movie-rec-466x.onrender.com" or "http://127.0.0.1:8000"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(
    page_title="Movie Recommender", 
    page_icon="🎬", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================
# FUTURISTIC STYLES
# =============================
st.markdown(
    """
<style>
    /* Import futuristic font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container styling */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1400px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Glass morphism effect */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 20px;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.4);
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    /* Movie card styling */
    .movie-card {
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 15px;
        transition: all 0.3s ease;
        cursor: pointer;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .movie-card:hover {
        transform: translateY(-8px);
        border-color: rgba(255, 255, 255, 0.4);
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    }
    
    .movie-title {
        font-size: 0.95rem;
        font-weight: 600;
        line-height: 1.3rem;
        margin-top: 10px;
        color: white;
        text-align: center;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }
    
    /* Gradient text */
    .gradient-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
    }
    
    /* Futuristic button */
    .futuristic-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 25px;
        padding: 10px 25px;
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .futuristic-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0.95) 100%);
        backdrop-filter: blur(10px);
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 25px;
        color: white;
        padding: 12px 20px;
        font-size: 16px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        color: white;
    }
    
    /* Divider styling */
    hr {
        background: linear-gradient(90deg, transparent, #667eea, #764ba2, transparent);
        height: 2px;
        border: none;
    }
    
    /* Animation for loading */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading {
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 20px;
        font-size: 0.8rem;
        color: white;
        font-weight: 600;
        margin: 5px;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2, #667eea);
    }
</style>
""",
    unsafe_allow_html=True,
)

# =============================
# STATE + ROUTING
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"
if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None
if "search_animation" not in st.session_state:
    st.session_state.search_animation = False

qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")
if qp_view in ("home", "details"):
    st.session_state.view = qp_view
if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except:
        pass


def goto_home():
    st.session_state.view = "home"
    st.query_params["view"] = "home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(int(tmdb_id))
    st.rerun()


# =============================
# API HELPERS
# =============================
@st.cache_data(ttl=30)
def api_get_json(path: str, params: dict | None = None):
    try:
        r = requests.get(f"{API_BASE}{path}", params=params, timeout=25)
        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}: {r.text[:300]}"
        return r.json(), None
    except Exception as e:
        return None, f"Request failed: {e}"


def poster_grid(cards, cols=6, key_prefix="grid", title=None):
    if not cards:
        st.info("✨ No movies to show. Try another category!")
        return
    
    if title:
        st.markdown(f"<h3 style='color: white;'>{title}</h3>", unsafe_allow_html=True)
    
    rows = (len(cards) + cols - 1) // cols
    idx = 0
    for r in range(rows):
        colset = st.columns(cols)
        for c in range(cols):
            if idx >= len(cards):
                break
            m = cards[idx]
            idx += 1

            tmdb_id = m.get("tmdb_id")
            title_text = m.get("title", "Untitled")
            poster = m.get("poster_url")
            rating = m.get("vote_average", None)

            with colset[c]:
                st.markdown("<div class='movie-card'>", unsafe_allow_html=True)
                
                if poster:
                    st.image(poster, use_column_width=True)
                else:
                    st.markdown("<div style='height: 250px; background: rgba(255,255,255,0.05); border-radius: 10px; display: flex; align-items: center; justify-content: center;'>🎬 No Poster</div>", unsafe_allow_html=True)
                
                if rating:
                    st.markdown(f"<div style='text-align: center; margin: 5px 0;'><span class='badge'>⭐ {rating:.1f}</span></div>", unsafe_allow_html=True)
                
                if st.button("🎬 Open", key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}", use_container_width=True):
                    if tmdb_id:
                        goto_details(tmdb_id)

                st.markdown(f"<div class='movie-title'>{title_text}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append(
                {
                    "tmdb_id": tmdb["tmdb_id"],
                    "title": tmdb.get("title") or x.get("title") or "Untitled",
                    "poster_url": tmdb.get("poster_url"),
                    "vote_average": tmdb.get("vote_average"),
                }
            )
    return cards


def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    keyword_l = keyword.strip().lower()

    if isinstance(data, dict) and "results" in data:
        raw = data.get("results") or []
        raw_items = []
        for m in raw:
            title = (m.get("title") or "").strip()
            tmdb_id = m.get("id")
            poster_path = m.get("poster_path")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": f"{TMDB_IMG}{poster_path}" if poster_path else None,
                    "release_date": m.get("release_date", ""),
                    "vote_average": m.get("vote_average"),
                }
            )
    elif isinstance(data, list):
        raw_items = []
        for m in data:
            tmdb_id = m.get("tmdb_id") or m.get("id")
            title = (m.get("title") or "").strip()
            poster_url = m.get("poster_url")
            if not title or not tmdb_id:
                continue
            raw_items.append(
                {
                    "tmdb_id": int(tmdb_id),
                    "title": title,
                    "poster_url": poster_url,
                    "release_date": m.get("release_date", ""),
                    "vote_average": m.get("vote_average"),
                }
            )
    else:
        return [], []

    matched = [x for x in raw_items if keyword_l in x["title"].lower()]
    final_list = matched if matched else raw_items

    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        rating = f"⭐ {x.get('vote_average', 0):.1f}" if x.get('vote_average') else ""
        label = f"{x['title']} ({year}) {rating}" if year else f"{x['title']} {rating}"
        suggestions.append((label, x["tmdb_id"]))

    cards = [
        {
            "tmdb_id": x["tmdb_id"], 
            "title": x["title"], 
            "poster_url": x["poster_url"],
            "vote_average": x.get("vote_average")
        }
        for x in final_list[:limit]
    ]
    return suggestions, cards


# =============================
# SIDEBAR
# =============================
with st.sidebar:
    st.markdown("<h1 style='text-align: center; margin-bottom: 20px;'>🎬 CineMate</h1>", unsafe_allow_html=True)
    
    if st.button("🏠 Home", use_container_width=True):
        goto_home()
    
    st.markdown("---")
    st.markdown("### 🎯 Discovery")
    home_category = st.selectbox(
        "Explore",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
        index=0,
        help="Choose your movie discovery category"
    )
    
    grid_cols = st.slider("🎨 Grid Density", 3, 8, 5, help="Adjust how many movies per row")
    
    st.markdown("---")
    st.markdown("### 📊 Stats")
    st.markdown("<div class='glass-card' style='text-align: center;'>", unsafe_allow_html=True)
    st.metric("Movies Available", "10K+", delta="🎬")
    st.metric("Daily Updates", "50+", delta="✨")
    st.markdown("</div>", unsafe_allow_html=True)

# =============================
# HEADER
# =============================
st.markdown(
    """
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 class='gradient-text' style='font-size: 3.5rem; margin-bottom: 10px;'>🎬 CineMate</h1>
        <p style='color: rgba(255,255,255,0.8); font-size: 1.2rem;'>Your AI-Powered Movie Companion</p>
        <p style='color: rgba(255,255,255,0.6);'>Discover, Explore, and Fall in Love with Cinema</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# ==========================================================
# VIEW: HOME
# ==========================================================
if st.session_state.view == "home":
    # Hero section with animated search
    st.markdown(
        """
        <div class='glass-card' style='text-align: center; margin-bottom: 30px;'>
            <h2 style='color: white;'>✨ Find Your Next Favorite Movie</h2>
            <p style='color: rgba(255,255,255,0.8);'>Search by title, genre, or mood</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    typed = st.text_input(
        "", 
        placeholder="🔍 Type a movie title... (e.g., Inception, The Dark Knight, Interstellar)",
        label_visibility="collapsed"
    )

    # SEARCH MODE
    if typed.strip():
        if len(typed.strip()) < 2:
            st.caption("✨ Type at least 2 characters for suggestions...")
        else:
            with st.spinner("🔍 Searching the galaxy of movies..."):
                data, err = api_get_json("/tmdb/search", params={"query": typed.strip()})

            if err or data is None:
                st.error(f"🚀 Search failed: {err}")
            else:
                suggestions, cards = parse_tmdb_search_to_cards(
                    data, typed.strip(), limit=24
                )

                if suggestions:
                    st.markdown("### 💡 Quick Suggestions")
                    labels = ["-- Select a movie --"] + [s[0] for s in suggestions]
                    selected = st.selectbox("", labels, index=0)

                    if selected != "-- Select a movie --":
                        label_to_id = {s[0]: s[1] for s in suggestions}
                        goto_details(label_to_id[selected])
                else:
                    st.info("✨ No suggestions found. Try another magical keyword!")

                if cards:
                    st.markdown("### 🎯 Search Results")
                    poster_grid(cards, cols=grid_cols, key_prefix="search_results")

        st.stop()

    # Enhanced HOME FEED with categories
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Featured Section
    st.markdown(
        f"""
        <div style='margin-bottom: 20px;'>
            <h2 style='color: white; display: inline-block;'>🔥 {home_category.replace('_',' ').title()}</h2>
            <span style='float: right; color: rgba(255,255,255,0.6);'>✨ Updated Daily</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    home_cards, err = api_get_json(
        "/home", params={"category": home_category, "limit": 24}
    )
    
    if err or not home_cards:
        st.error(f"🚀 Home feed failed: {err or 'Unknown error'}")
        st.stop()
    
    poster_grid(home_cards, cols=grid_cols, key_prefix="home_feed")
    
    # Add a footer with recommendations
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div class='glass-card' style='text-align: center;'>
                <h3>🎯 10K+</h3>
                <p>Movies in Database</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div class='glass-card' style='text-align: center;'>
                <h3>⚡ AI-Powered</h3>
                <p>Smart Recommendations</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            """
            <div class='glass-card' style='text-align: center;'>
                <h3>🔄 Real-time</h3>
                <p>Updates Every Day</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# ==========================================================
# VIEW: DETAILS
# ==========================================================
elif st.session_state.view == "details":
    tmdb_id = st.session_state.selected_tmdb_id
    if not tmdb_id:
        st.warning("✨ No movie selected. Let's go back!")
        if st.button("← Back to Home"):
            goto_home()
        st.stop()

    # Back button
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Back", use_container_width=True):
            goto_home()

    with st.spinner("🎬 Loading movie details..."):
        data, err = api_get_json(f"/movie/id/{tmdb_id}")
    
    if err or not data:
        st.error(f"🚀 Could not load details: {err or 'Unknown error'}")
        st.stop()

    # Hero section with backdrop
    if data.get("backdrop_url"):
        st.markdown(
            f"""
            <div style='
                background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url({data["backdrop_url"]});
                background-size: cover;
                background-position: center;
                border-radius: 20px;
                padding: 50px;
                margin-bottom: 30px;
            '>
                <h1 style='color: white; font-size: 3rem; margin-bottom: 10px;'>{data.get('title', '')}</h1>
                <p style='color: rgba(255,255,255,0.9); font-size: 1.1rem;'>{data.get('tagline', '')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Main content
    left, right = st.columns([1, 2], gap="large")

    with left:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        if data.get("poster_url"):
            st.image(data["poster_url"], use_column_width=True)
        else:
            st.markdown("<div style='height: 300px; background: rgba(255,255,255,0.05); border-radius: 15px; display: flex; align-items: center; justify-content: center;'>🎬 No Poster Available</div>", unsafe_allow_html=True)
        
        # Quick stats
        if data.get("vote_average"):
            st.markdown(f"<div style='text-align: center; margin-top: 15px;'><span class='badge'>⭐ {data['vote_average']:.1f}/10</span></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        # Movie info
        if data.get("release_date"):
            st.markdown(f"**📅 Release Date:** {data['release_date']}")
        if data.get("runtime"):
            st.markdown(f"**⏱️ Runtime:** {data['runtime']} minutes")
        if data.get("genres"):
            genres = ", ".join([g["name"] for g in data.get("genres", [])])
            st.markdown(f"**🎭 Genres:** {genres}")
        if data.get("production_companies"):
            companies = ", ".join([c["name"] for c in data.get("production_companies", [])[:3]])
            st.markdown(f"**🏢 Production:** {companies}")
        
        st.markdown("---")
        st.markdown("### 📖 Synopsis")
        st.write(data.get("overview") or "No overview available. This movie is waiting to be discovered!")
        
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    
    # Recommendations section
    st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>✨ You Might Also Like ✨</h2>", unsafe_allow_html=True)
    
    title = (data.get("title") or "").strip()
    if title:
        with st.spinner("🤖 Finding similar movies..."):
            bundle, err2 = api_get_json(
                "/movie/search",
                params={"query": title, "tfidf_top_n": 12, "genre_limit": 12},
            )

        if not err2 and bundle:
            tfidf_cards = to_cards_from_tfidf_items(bundle.get("tfidf_recommendations"))
            if tfidf_cards:
                poster_grid(
                    tfidf_cards,
                    cols=grid_cols,
                    key_prefix="details_tfidf",
                    title="🎯 Based on Your Interest"
                )
            
            genre_cards = bundle.get("genre_recommendations", [])
            if genre_cards:
                poster_grid(
                    genre_cards,
                    cols=grid_cols,
                    key_prefix="details_genre",
                    title="🎭 More in This Genre"
                )
        else:
            st.info("✨ Showing genre-based recommendations...")
            genre_only, err3 = api_get_json(
                "/recommend/genre", params={"tmdb_id": tmdb_id, "limit": 18}
            )
            if not err3 and genre_only:
                poster_grid(
                    genre_only, 
                    cols=grid_cols, 
                    key_prefix="details_genre_fallback",
                    title="🎬 Similar Movies"
                )
            else:
                st.warning("🚀 No recommendations available right now. Try exploring other movies!")
    else:
        st.warning("✨ No title available to compute recommendations.")