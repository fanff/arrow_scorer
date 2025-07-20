import streamlit as st


def custom_css():
    st.markdown(
        """
        <style>
            div[data-testid="stColumn"] {
                width: fit-content !important;
                flex: unset;
                min-width: 70px !important;
            }
            div[data-testid="stColumn"] * {
                width: fit-content !important;
            }
        
            span[data-testid="stIconEmoji"] {
                margin: 0px 0.15rem 0px 0px;
            }
            div[data-testid="stMarkdownContainer"] {
                line-height: 1;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
