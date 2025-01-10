import numpy as np
import streamlit as st

pages = {
    "outsourcing func": [
        st.Page("golden.py", title="Golden label"),
        st.Page("image_resize.py", title="Image Resize"),
        st.Page("translate.py",title="Translate")
    ],
}

if __name__ == "__main__":
    st.set_page_config(layout="wide",
                   page_title='internal Apps')
    pg = st.navigation(pages)
    pg.run()