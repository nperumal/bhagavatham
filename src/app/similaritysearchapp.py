import streamlit as st
from job.similaritysearch import query
import pandas as pd
from config import *
import requests

st.set_page_config(page_title="చెప్పండి")

def generate_response(input_text):
    response = requests.post(f'{ANN_INDEX_SERVER}search', json={'text': text})
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None
  
with st.sidebar.title('భాగవతం'):
     st.write("బమ్మెర పోతానా")
     st.write("")
     st.write("""మందార మకరంద మాధుర్యమునఁ దేలు మధుపంబు వోవునే మదనములకు
నిర్మల మందాకినీ వీచికలఁ దూఁగు రాయంచ సనునె తరంగిణులకు
లలిత రసాలపల్లవ ఖాది యై చొక్కు కోయిల సేరునే కుటజములకు
బూర్ణేందు చంద్రికా స్ఫురిత చకోరక మరుగునే సాంద్ర నీహారములకు
అంబుజోదర దివ్య పాదారవింద
చింతనామృత పానవిశేష మత్త
చిత్త మేరీతి నితరంబు జేరనేర్చు
వినుతగుణశీల! మాటలు వేయునేల?""")

submitted = False

with st.form('my_form'):
  text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')
  submitted = st.form_submit_button('Submit')
  
if submitted and text:
   # Call the REST service
   response = generate_response(text)
   # Check if the request was successful
   if response != None:
        poem, poemtitle, context, meaning, poemtitle_translation, context_translation, meaning_translation, audio_path = response[0]

        st.audio(f"{AUDIO_ROOT}{audio_path}", format="audio/mpeg", loop=False)

        poem = poem.replace("\n", "  \n")
        with st.container(height=200):
                st.write(poemtitle)
                st.write("")
                st.write(poem)

        with st.expander("అర్థం & సందర్భం (Meaning & Context)"):
                st.write(meaning)
                st.write("")
                st.write('['+meaning_translation+']')
                st.write("")
                st.write(context)
                st.write("")
                st.write('['+context_translation+']')

