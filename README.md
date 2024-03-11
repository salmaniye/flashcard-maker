# Flashcard Maker

A web app based on streamlit deployed at [https://flashcard-maker.streamlit.app](https://flashcard-maker.streamlit.app)

This web app was built on Streamlit and adapted from: https://github.com/TomJohnH/streamlit-po
I kept the question and answer reveal mechanisms as well as the search engine.

## Changes from original repo:

- Removed CSS
- Added option for the user to create their own flashcards by uploading a CSV dataset file
- Added option to divide the total number of questions into a specified number of days
- Added option to randomize between questions and answers (i.e. some answers become questions)
- Integrated an RNG seed to maintain consistency in dataset loading, ensuring users won't encounter previously seen question/answer pairs when reloading.

## CSV File requirements

The CSV file must contain only 2 columns, the first column should be for questions, and the second column for answers.

## Change log

11.03.2024
- Renamed "days" into "splits"
- Added feature to combine with previous splits, along with option to choose first split
- Moved some UI elements to the sidebar
- Moved current split's questions to its own tab
