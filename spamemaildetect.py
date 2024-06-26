from random import choices
import streamlit as st
import pickle
from sklearn.feature_extraction.text import CountVectorizer
import base64

# These modules are causing issues when hosting on Streamlit
# from win32com.client import Dispatch
# import pythoncom
# import win32api

# No need to initialize COM objects when running on Streamlit
# pythoncom.CoInitialize()

# Commenting out the speak function as it requires win32com which is not compatible with Streamlit
# def speak(text):
#     speak = Dispatch(("SAPI.SpVoice"))
#     speak.Speak(text)

# Load the model and CountVectorizer




model = pickle.load(open('model.pkl', 'rb'))
cv = pickle.load(open('vectorizer.pkl', 'rb'))

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

def main():
    # Adjust the width of the logo column as needed
    logo_col, title_col = st.columns([0.2, 1])  

    with logo_col:
        # Adjust width as needed
        st.image("CyberBlockLogo.png", width=100)  

    with title_col:
        st.title(" :violet[SPAM EMAIL DETECTOR]")
        st.write("Build By MAKSQUARE")

    activities = ["SPAM EMAIL DETECTION", "About"]
    choice = st.sidebar.selectbox("CHOOSE YOUR REQUIREMENT", activities)
    
    if choice == "SPAM EMAIL DETECTION":
        msg = st.text_input("Enter The Suspicious Email:")
        
        if st.button("CHECK"):
            data = [msg]
            vec = cv.transform(data).toarray()
            result = model.predict(vec)
            if result[0] == 0:
                autoplay_audio("ttsmake.mp3")
                # st.components.v1.html(f'<audio autoplay><source src="{audio_file_path}" type="audio/mp3"></audio>')
                # st.markdown(f"""<script>var audio=new Audio("{audio_file_path}");audio.play()<script>""", unsafe_allow_html=True)
                # st.markdown(f"""<script>var audio=new Audio("{audio_file_path}");
                #          audio.play()<script>""")
                st.success("This is Not A Spam Email")
            else:
                
                autoplay_audio("spam.mp3")
                st.error("This is A Spam Email")

                
    else:
        st.write(':green[Spam Email Detection]')
        st.write("Filter out Suspicious Emails")
        st.write('Filter out you Suspicious By using this Spam Mail Detector Tool that will tell You Weather a Email is a Malicious Email or not. This Spam Email detector saves users valuable time and enhances productivity by ensuring that only relevant and legitimate messages reach their inboxes. Moreover, they serve as a frontline defense against various cyber threats, such as phishing attempts, malware distribution, and scams, thereby bolstering security and protecting sensitive information. Ultimately, This Email Spam detector fosters a positive email experience by delivering a clean and trustworthy inbox, thereby enhancing user satisfaction and trust in email communication.')

main()