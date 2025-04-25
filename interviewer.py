from bridge import get_interview
import uuid


class Interviewer:

    def __init__(self, st):
        self.st = st
        self.st.title("Technical Interviewer")
        # Two columns
        col1, col2, col3 = self.st.columns(3)


        # Text input for name
        with col1:
            self.user_name = self.st.text_input("Enter your name:", placeholder="Name", key="Name")

        # Dropdown for number of questions
        with col2:
            self.max_questions = self.st.selectbox("Select number of questions:", [3, 5, 15, 25, 35], key="Max questions")

        # Dropdown for number of questions
        with col3:
            self.difficulty = self.st.selectbox("Select difficulty level:", ['Easy', 'Intermediate', 'Expert', 'Mix'],
                                      key="Difficulty Type")

        # Input for technologies
        self.technologies = self.st.text_input("Enter technologies (comma separated, minimum 1) :",
                                     placeholder="Java, Python, ...", key="Technology")
        self.subjects = [tech.strip() for tech in self.technologies.split(',') if tech.strip()]

        self.first_question = f"Hi {self.user_name} could you please provide brief introduction about yourself and provide information on your skills? "


        # Initialize session state variables
        if "chat_started" not in self.st.session_state:
            self.st.session_state.chat_started = False

        if "first_entry" not in self.st.session_state:
            self.st.session_state.first_entry = True

        if self.st.button("Begin Interview"):
            if self.user_name.strip() == "" or len(self.subjects) == 0:
                self.st.error("Name and Technology are required.")
                self.st.session_state.chat_started = False
            else:
                self.st.session_state.chat_started = True

        if "messages" not in st.session_state:
            self.st.session_state.messages = []

        if "num_questions" not in st.session_state:
            self.st.session_state.num_questions = 1

        if "new_question" not in st.session_state:
            self.st.session_state.new_question = ""

        if "user_id" not in st.session_state:
            self.st.session_state.user_id = str(uuid.uuid4())

        if "show_prompt" not in st.session_state:
            self.st.session_state.show_prompt = True


    def __call__(self):
        if self.st.session_state.chat_started:

            if self.st.session_state.first_entry is True:
                self.st.session_state.new_question = self.first_question
                self.st.session_state.messages.append({"role": "interviewer", "content": self.first_question})
                self.st.session_state.first_entry = False


            for message in self.st.session_state.messages:
                with self.st.chat_message(message["role"]):
                    self.st.markdown(message['content'])

            if self.st.session_state.show_prompt:
                prompt = self.st.chat_input("Provide your answer here:")

                if prompt:

                    with self.st.chat_message("user"):
                        self.st.markdown(prompt)

                    self.st.session_state.messages.append({"role": "user", "content": prompt})

                    data = {
                        "difficulty": self.difficulty,
                        "user_id": self.st.session_state.user_id,
                        "user_name": self.user_name,
                        "subjects": self.subjects,
                        "human_answer": prompt,
                        "previous_question": self.st.session_state.new_question,
                        "max_questions": self.max_questions,
                        "num_questions": self.st.session_state.num_questions
                    }
                    placeholder = self.st.empty()
                    placeholder.info("Interviewer typing..... ")
                    result = get_interview(data)
                    print("result-------", result)
                    placeholder.markdown('')

                    interview_output = ""
                    if result is None:
                        interview_output = f"The interview is over [Generate_Results](?result={self.st.session_state.user_id})"
                        self.st.session_state.show_prompt = False
                    elif result[0] == 'NA':
                        interview_output = result[1]
                        self.st.session_state.new_question = interview_output
                        self.st.session_state.num_questions = result[2]
                    else:
                        interview_output = result

                    with self.st.chat_message("interviewer"):
                        self.st.markdown(interview_output)

                    self.st.session_state.messages.append({"role": "interviewer", "content": interview_output})
                    self.st.rerun()