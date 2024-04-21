from random import choices
import streamlit as st
import pickle
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import os
import pyttsx3
import sys

import platform
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


def speak(text):
    if st.session_state.is_windows:
        speak_windows(text)
    elif st.session_state.is_mac:
        speak_mac(text)
    else:
        st.error("Unsupported operating system")

def speak_mac(text):
    import os
    os.system(f'say {text}')

def speak_windows(text):
    import pyttsx3
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


model = pickle.load(open('model.pkl', 'rb'))
cv = pickle.load(open('vectorizer.pkl', 'rb'))

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
                st.success("This is Not A Spam Email")
                speak("THANK GOD This is Not A Spam Email")
                # Commenting out the speak function as it requires win32com which is not compatible with Streamlit
                # speak(
            else:
                st.error("This is A Spam Email")
                # Commenting out the speak function as it requires win32com which is not compatible with Streamlit
                speak("ALERT This is A Spam Email")
                
    else:
        st.write(':green[Spam Email Detection]')
        st.write("Filter out Suspicious Emails")
        st.write('Filter out you Suspicious By using this Spam Mail Detector Tool that will tell You Weather a Email is a Malicious Email or not. This Spam Email detector saves users valuable time and enhances productivity by ensuring that only relevant and legitimate messages reach their inboxes. Moreover, they serve as a frontline defense against various cyber threats, such as phishing attempts, malware distribution, and scams, thereby bolstering security and protecting sensitive information. Ultimately, This Email Spam detector fosters a positive email experience by delivering a clean and trustworthy inbox, thereby enhancing user satisfaction and trust in email communication.')

if __name__ == "__main__":
    # Detect the operating system and set session state flags accordingly
    st.session_state.is_windows = False
    st.session_state.is_mac = False

    if st._is_running_with_streamlit:
        if st._is_running_on_darwin:
            st.session_state.is_mac = True
        elif st._is_running_on_windows:
            st.session_state.is_windows = True

    main()