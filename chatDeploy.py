import streamlit as st 
import shelve 
import warnings 
warnings.filterwarnings('ignore')
import google.generativeai as genai
from knowledge import googleModelKnowledge as myKnowledge


genai.configure(api_key="AIzaSyCbwfzBjY9ucaZdPd8apShPgrF-EuN_sPQ")


# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
  system_instruction=myKnowledge()
)



def saveHistory(chatHistory, filename='ChatHistory'):
    with shelve.open(filename) as db:
        db['chatHistory'] = chatHistory

def loadHistory(filename='chatHistory'):
    with shelve.open(filename) as db:
        return db.get('chatHistory', [])

history_ = loadHistory()

chat_session = model.start_chat(
  history=history_
)

st.markdown("<h1 style='color: #780C28; font-size: 36px ; font-family: Verdana; text-align: center;'>CHATBOT POWERED BY GEMINI</h1>", unsafe_allow_html = True)
st.markdown("<h3 style='margin-top: -20px; color: #1D1616; font-size: 24px ; font-family: cursive; text-align: center;'>Built By JIT Group</h3>", unsafe_allow_html = True)

st.markdown('<br><br>', unsafe_allow_html=True)

imageColumn, chatColumn = st.columns([2,3])
with imageColumn:
    st.image('pngwing.com(6).png', width = 300)
with chatColumn:
    userInput = st.chat_input('Ask your question')
    if userInput:
        userOutput = st.chat_message(name='user')
        userOutput.write(userInput)
        response = chat_session.send_message(userInput)
        history_.append({"role": "user", "parts": [userInput]})
        history_.append({"role": "model","parts": [response]})
        saveHistory(history_)
        
        modelOutput = st.chat_message(name='ai')
        modelOutput.write(response.text)


