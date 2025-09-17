import streamlit as st
from . import config


def inject_global_css():
    st.markdown(
        """
        <style>
        /* Global font smoothing and base sizing */
        html, body, [class*="css"]  {
            -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale;
        }
        /* Hero and header styling */
        .ht-hero {
            background: linear-gradient(135deg, #0ea5e9 0%, #22c55e 100%);
            border-radius: 18px;
            padding: 28px 28px;
            color: white;
            box-shadow: 0 10px 25px rgba(0,0,0,0.10);
        }
        .ht-card {
            border-radius: 14px;
            padding: 18px 18px;
            background: rgba(255,255,255,0.75);
            border: 1px solid rgba(0,0,0,0.05);
            backdrop-filter: blur(6px);
        }
        .ht-pill {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 999px;
            background: rgba(255,255,255,0.2);
            font-size: 0.8rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_brand_header():
    logo_path = config.get_logo_path()
    left, right = st.columns([1, 10])
    with left:
        if logo_path:
            st.image(logo_path, width=100)
    with right:
        st.title(config.APP_NAME)


def ensure_authenticated():
    """Simple demo auth. In production, rely on Streamlit secrets or external auth."""
    if config.ALLOW_DEMO_LOGIN:
        # Persist a trivial demo login state
        if st.session_state.get("password_correct") is None:
            st.session_state["password_correct"] = True
        return True
    # If demo not allowed, require prior auth mechanism
    if not st.session_state.get("password_correct"):
        st.warning("Please login first.")
        st.stop()
        return False
    return True