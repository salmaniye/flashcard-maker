import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import random
import pandas as pd

# -------------- APP CONFIG ---------------

st.set_page_config(page_title="Flashcards Maker", page_icon="📖")

# ---------------- functions ----------------

# callbacks
def callback():
    st.session_state.button_clicked = True

def callback2():
    st.session_state.button2_clicked = True

# ---------------- SESSION STATE ----------------

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

if "button2_clicked" not in st.session_state:
    st.session_state.button2_clicked = False

if "q_no" not in st.session_state:
    st.session_state.q_no = -1

if "q_no_temp" not in st.session_state:
    st.session_state.q_no_temp = -1

# ---------------- SIDEBAR ----------------
with st.sidebar:
    uploaded_csv = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_csv:
        qa_df = pd.read_csv(uploaded_csv) # load questions and answers from CSV file
        
        qa_df_rand = qa_df.sample(frac=1, random_state=2).reset_index(drop=True) # randomize with set random state

        div_days = st.number_input('Number of days to divide the questions on: ', value=48)
        st.write('The current number of days is ', div_days)

        split_qa = np.array_split(qa_df_rand,div_days) # split it into days

# ---------------- Main page ----------------

tab1, tab2 = st.tabs(["Flashcards", "Search engine"])

with tab1:
    if uploaded_csv:
        # st.title("Product Owner Interview Questions Flashcards")
        no = len(qa_df)
        st.caption("There are currently " + str(no) + " questions in the database")
        
        day_number = st.slider('Day Number', 1, div_days, 1)
        split_qa_rand = split_qa[day_number-1].reset_index(drop=True)

        # Randomize between words and definitions
        agree_to_randomize = st.checkbox("Do you want to randomize between questions and answers (i.e. some answers become questions)?")
        if agree_to_randomize:
            split_qa_rand.iloc[:,0] = 'Question: ' + split_qa_rand.iloc[:,0].astype(str)
            split_qa_rand.iloc[:,1] = 'Answer: ' + split_qa_rand.iloc[:,1].astype(str)
            # default seed 48
            split_qa_rand = split_qa_rand.apply(np.random.default_rng(seed=32).permutation,axis=1,result_type='expand').set_axis(split_qa_rand.columns,axis=1)
        
        with st.expander(f"See all questions for day {day_number}"):
            st.write(split_qa_rand)

        # ---------------- Questions & answers logic ----------------
        col1, col2 = st.columns(2)
        with col1:
            question = st.button("Draw question", on_click=callback, key="Draw", use_container_width=True)
        with col2:
            answer = st.button("Show answer", on_click=callback2, key="Answer", use_container_width=True)

        if question or st.session_state.button_clicked:
            # randomly select question number
            no_split = len(split_qa_rand)
            st.session_state.q_no = random.randint(0, no_split - 1)

            # this 'if' checks if algorithm should use value from temp or new value (temp assigment in else)
            if st.session_state.button2_clicked:
                st.markdown(
                    f'<div class="blockquote-wrapper"><div class="blockquote"><h1>{split_qa_rand.iloc[st.session_state.q_no_temp,0]}</h1><h4>&mdash; Question no. {st.session_state.q_no_temp+1}</em></h4></div></div>',
                    unsafe_allow_html=True,
                )
                
            else:
                st.markdown(
                    f'<div class="blockquote-wrapper"><div class="blockquote"><h1>{split_qa_rand.iloc[st.session_state.q_no,0]}</h1><h4>&mdash; Question no. {st.session_state.q_no+1}</em></h4></div></div>',
                    unsafe_allow_html=True,
                )
                # keep memory of question number in order to show answer
                st.session_state.q_no_temp = st.session_state.q_no

            if answer:
                st.markdown(
                    f"<div class='answer'><span style='font-weight: bold;'>Answer to question number {st.session_state.q_no_temp+1}</span><br><br>{split_qa_rand.iloc[st.session_state.q_no_temp,1]}</div>",
                    unsafe_allow_html=True,
                )
                st.session_state.button2_clicked = False


        st.markdown(
            '<div><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Abril+Fatface&family=Barlow+Condensed&family=Cabin&display=swap" rel="stylesheet"></div>',
            unsafe_allow_html=True,
        )

with tab2:
    if uploaded_csv:
        df = qa_df

        # Use a text_input to get the keywords to filter the dataframe
        text_search = st.text_input("Search in questions and answers from all days", value="")

        # Filter the dataframe using masks
        m1 = df.iloc[:,0].str.contains(text_search, case=False)
        m2 = df.iloc[:,1].str.contains(text_search, case=False)
        df_search = df[m1 | m2]

        # Show the cards
        N_cards_per_row = 2
        if text_search:
            for n_row, row in df_search.reset_index().iterrows():
                i = n_row % N_cards_per_row
                if i == 0:
                    st.write("---")
                    cols = st.columns(N_cards_per_row, gap="large")
                # draw the card
                with cols[n_row % N_cards_per_row]:
                    st.caption(f"Question {row['index']:0.0f}")
                    st.markdown(f"**{row.iloc[1].strip()}**")
                    with st.expander("Answer"):
                        st.markdown(f"{row.iloc[2].strip()}")