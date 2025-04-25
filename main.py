import streamlit as st
from interviewer import Interviewer
from bridge import get_evaluation

query_params = st.query_params
page = query_params
sum_marks = 0.0


if len(page)==0:
    interviewer = Interviewer(st)
    interviewer()

else:
    unique_id = page['result']
    st.title("Results")
    results= get_evaluation(unique_id)
    print(results)

    for question_number, result in enumerate(results, start=1):
        question = result[0]
        answer = result[1]
        feedback = result[2]
        marks = result[3]
        sum_marks += float(marks)

        st.markdown(f"**Question No: {question_number}**")
        st.markdown(f"**Question:**  {question}")
        st.markdown(f"**Provided Answer:**  {answer}")
        st.markdown(f"**Evaluation by interviewer:** {feedback}")
        st.markdown(f"**Marks(out of 5):**  {marks}")
        st.markdown("<br><hr><br>", unsafe_allow_html=True)

    print(sum_marks, len(results))
    percent = (sum_marks/(len(results)*5.0))*100
    print(percent)
    score_level = "Excellent" if percent > 85 else  "Satisfactory" if (percent <= 85  and percent > 75 ) else "Needs improvement"
    st.markdown("###    Overall Result")
    st.markdown(f"**Acheived: {percent:.2f}% - {score_level}**")