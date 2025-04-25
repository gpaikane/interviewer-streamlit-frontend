The repo contains frontend code which facilitates interaction like a chatbot of interviewer and interviewee. The Goal of the app is to prepare interviwee for the interview.

Currently the frontend is hosted on **AWS EC2** http://51.20.190.247/

The backend repo is located here: https://github.com/gpaikane/interviewr-fastapi and backend is hosted on **AWS EC2**: http://51.20.129.124/docs

**Details**
As part of the code a streamlit app is created which takes input of Name, technology, difficulty level, takes prompt from the interviewee.
Sends the details to backend which is created using fast api and gets the next question from LLMs

Once the numer of questions selected in drop down are answered then a report is generated which basically fetches stored evaluation from database and displays on the page.

command used to start streamlit server : `streamlit run main.py`
