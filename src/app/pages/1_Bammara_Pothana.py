import streamlit as st
import pandas as pd
import requests
from config import *

st.set_page_config(layout="centered")

@st.cache_data(show_spinner=False)
def load_data():
    response = requests.get(f'{ANN_INDEX_SERVER}poems')
    if response.status_code == 200:
        data = pd.DataFrame(response.json(), columns=['poem', 'poemtitle', 'context', 'meaning', 'poemtitle_translation', 'context_translation', 'meaning_translation', 'audiopath'])
        return data, len(data)
    else:
        return None, 0

@st.cache_data(show_spinner=False)
def split_frame(input_df, rows):
    df = [input_df.loc[i : i + rows - 1, :] for i in range(0, len(input_df), rows)]
    return df

dataset, total_pages  = load_data()

# top_menu = st.columns(3)
# with top_menu[0]:
#     search_field = st.
#     sort = st.radio("Sort Data", options=["Yes", "No"], horizontal=1, index=1)
# if sort == "Yes":
#     with top_menu[1]:
#         sort_field = st.selectbox("Sort By", options=dataset.columns)
#     with top_menu[2]:
#         sort_direction = st.radio(
#             "Direction", options=["⬆️", "⬇️"], horizontal=True
#         )
#     dataset = dataset.sort_values(
#         by=sort_field, ascending=sort_direction == "⬆️", ignore_index=True
#     )
pagination = st.container()

# bottom_menu = st.columns((4, 1, 1))
# with bottom_menu[2]:
#     batch_size = st.selectbox("Page Size", options=[25, 50, 100])
# with bottom_menu[1]:
#     total_pages = (
#         int(len(dataset) / batch_size) if int(len(dataset) / batch_size) > 0 else 1
#     )
#     current_page = st.number_input(
#         "Page", min_value=1, max_value=total_pages, step=1
#     )
# with bottom_menu[0]:
#     st.markdown(f"Page **{current_page}** of **{total_pages}** ")

# current_poem = st.number_input(
#         "Poem", min_value=1, max_value=total_pages, step=1
#     )
# pages = split_frame(dataset, batch_size)
# pagination.dataframe(data=pages[current_page - 1], use_container_width=True)
top_menu = st.columns([.2,.8])
poem_title_menu = st.columns([.6, .4])
poem_menu = st.columns(1)
poem_meaning_menu = st.columns([.5, .5])
poem_context_menu = st.columns([.5, .5])

with top_menu[0]:
    current_poem = st.number_input(
        "Poem", min_value=1, max_value=total_pages, step=1, key='current_poem'
    )

with poem_title_menu[0]:
    st.write(dataset.loc[current_poem-1, 'poemtitle'])

with poem_title_menu[1]:
    st.audio(f"{AUDIO_ROOT}{dataset.loc[current_poem-1, 'audiopath']}", format="audio/mpeg", loop=False)

with poem_menu[0]:
    st.write(dataset.loc[current_poem-1, 'poem'].replace("\n", "  \n"))

with poem_meaning_menu[0]:
    st.write(dataset.loc[current_poem-1, 'meaning'])
with poem_meaning_menu[1]:
    st.write(dataset.loc[current_poem-1, 'meaning_translation'])

with poem_context_menu[0]:
    st.write(dataset.loc[current_poem-1, 'context'])
with poem_context_menu[1]:
    st.write(dataset.loc[current_poem-1, 'context_translation'])