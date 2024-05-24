import streamlit as st


st.set_page_config(page_title="DGA Detector", 
                   page_icon="👋", 
                   layout="centered")

st.write("# Welcome to DGA Detection Application! 👋")

st.markdown(
    """
    The purpose of this app is to tell DGA-generated and non-DGA-generated domains apart using a combination of 
    linguistic features that characterize the domain name. By transforming raw domain strings to Machine Learning features, 
    it can be determined whether a given domain is legit or not.

    **👈 Go to the DGA app** to see how it works!
    ### Want to learn more about DGA:question:
    - 👈 Jump into the Documentation section and see related work in References
    - :eyes: And if you want to know the model running behind the scences check out the [source code](https://github.com/dorianDraper/DGA-Detection-final)
"""
)

st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center; margin-top: 200px;">
        <span style="margin-right: 20px;">© Powered & Developed by <b>Jorge Payà</b></span>
    </div>
    """, unsafe_allow_html=True)