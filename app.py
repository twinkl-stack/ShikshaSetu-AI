from flask import Flask, render_template, request
from google import genai
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
load_dotenv()
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)
    
app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
quiz_count = 0
story_count = 0
summary_count = 0
studyplan_count = 0
def ask_gemini(prompt):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        print("GEMINI ERROR =", e)
        return f"ERROR: {e}"  
@app.route("/")
def welcome():
    return render_template("welcome.html")


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/school")
def school():
    return render_template("school_form.html")


@app.route("/college")
def college():
    return render_template("college_form.html")    

@app.route("/dashboard", methods=["GET", "POST"])
def home():
    global quiz_count, summary_count, studyplan_count, story_count,latest_mock_test
    

    result = ""
    mock_test = ""
    student_type = request.args.get("student_type", "")
    student_class = request.args.get("student_class", "")
    subject = request.args.get("subject", "")

    badge = "🌱 Beginner"
    xp = 0
    level = 1
    xp_percent = 0

    if  request.method == "POST":
           image = request.files.get("question_image")
           subject = request.form.get("subject","" )
           
           notes = request.form.get("notes", "")
           
           action = request.form.get("action", "")
           difficulty = request.form.get("difficulty", "")
           test_type = request.form.get("test_type", "")
           chapter = request.form.get("chapter", "")
           student_class = request.form.get("student_class", "")
           student_type = request.form.get("student_type", student_type)
        
           print("Student Type =", student_type)
           print("ACTION =", action)
           
           if action == "explain_hindi":
            prompt = f"""
            Explain the following study notes in simple Hindi for a student:

            Class: {student_class}
            Subject: {subject}

            Notes:
            {notes}
            """
            result = ask_gemini(prompt)

           elif action == "explain_english":
            prompt = f"""
            Explain the following study notes in simple English for a student.
            Class: {student_class}
            Subject: {subject}

            Notes:
            {notes}
            """
            result = ask_gemini(prompt)

        
           elif action == "generate_summary":
            summary_count += 1

            prompt = f"""
            Create a short and easy summary of these notes.
            Class: {student_class}
            Subject: {subject}
            
            Notes:
            {notes}

            Make it student-friendly with bullet points.
            """

            result = ask_gemini(prompt)

           elif action == "study_plan":
            studyplan_count += 1

            prompt = f"""
            Create a personalized study plan for a student.

            Student Type: {request.form.get('student_type')}
            Class: {student_class}
            Subject: {subject}
            Difficulty: {difficulty}

            Notes:
            {notes}

           Your job is to become the student's personal study mentor.

            Create a personalized study guide based on:

            Class: {student_class}
            Subject: {subject}
            Difficulty: {difficulty}

            The guide must include:

            1. Today's Study Goal

            2. What should the student study first?

            3. Which feature of ShikshaSetu AI should be used?

            Example:

            📖 If subject is History, Geography, Political Science, Biology,
            English Literature, EVS or Business Studies:

            → First use Story Learning.

            ➜ Then use Summary.

            ➜ Finally attempt Mock Test.

            ---------------------------------------------------

            If subject is Mathematics, Physics, Chemistry,
            Accountancy, Economics or Computer Science:

            → First use Solve Question.

            ➜ Then use Summary.

            ➜ Finally attempt Mock Test.

            ---------------------------------------------------

            4. Estimated Study Time

            5. Revision Tips

            6. Motivation for today's study

            Keep the guide short, practical and student-friendly.

            Use simple Hinglish.
            Keep it practical and student-friendly.
            """
            result = ask_gemini(prompt)
           elif action == "mock_test":
            quiz_count += 1
            prompt = f"""
            You are an experienced CBSE, RBSE and Indian State Board paper setter and examiner.

            Generate a HIGH-QUALITY MOCK TEST.

            Student Details:
            Class: {student_class}
            Subject: {subject}
            Chapter: {chapter}
            Difficulty: {difficulty}
            Test Type: {test_type}
            Notes:
            {notes}
            Generate the paper according to the latest examination pattern generally followed by CBSE, RBSE and other major Indian State Boards.
            ========================
            QUESTION PAPER RULES
            ========================

            Generate ONLY the question paper.

            DO NOT write:
            - Answers
            - Hints
            - Solutions
            - Explanations
            - Marking scheme
            ========================
            MARKS & TIME RULES
            ========================

            Select suitable total marks automatically according to class and question pattern.

            - Classes 1–5: Around 20 marks
            - Classes 6–8: Around 30 marks
            - Classes 9–10: Around 40–50 marks
            - Classes 11–12: Around 70–80 marks

            Mention suitable exam duration automatically according to the total marks.
            
            ========================
            CLASS-WISE PATTERN
            ========================

            Class 1-4

           • Simple MCQs
           • Fill in the blanks
           • Match the following
           • Very short questions
           • Picture based questions (if applicable)
             
           ------------------------

            Class 5-8

            • MCQs
            • Fill in the blanks
            • True/False
            • Short Answer Questions
            • Long Answer Questions
            • Application Based Questions
            • Maths → Easy + Medium numericals

            ------------------------

            Class 9-10

            Generate according to Board Pattern.

            Include wherever applicable:

            • MCQs
            • Assertion Reason
            • Case Based Questions
            • Very Short Answer
            • Short Answer
            • Long Answer
            • Numericals (Maths & Science)
            • Map Questions (History/Geography when applicable)
            • Diagram Questions (Science where applicable)

            ------------------------

            Class 11-12

            Generate Board Style Paper.

            Include:

            • MCQs
            • Case Study
            • Competency Based Questions
            • Short Answer
            • Long Answer
            • Numericals
            • HOTS Questions

            ========================
            SUBJECT RULES
            ========================

            • Mathematics → More numericals and step-based questions.
            • Science → Conceptual, numerical and diagram-based questions where applicable.
            • Social Science → Map, source and case-based questions where applicable.
            • English/Hindi → Reading, Grammar, Writing Skills and Literature.
            • Commerce → Numerical and analytical questions.
           
            ========================
            FORMATTING RULES
            ========================

            The paper MUST look neat.

            Write exactly in this format.

            ================================

            📝 MOCK TEST

            Class:
            Subject:
            Chapter:
            Time:
            Maximum Marks:

            --------------------------------
            

            • Include:
            - Title
            - Class
            - Subject
            - Chapter
            - Time
            - Maximum Marks
            - General Instructions
            - Section A, B, C, D (as applicable)

            • Leave proper spacing between questions.
            • Number all questions correctly.
            • Make the paper look like a real board examination paper.
            • Return ONLY the formatted question paper.
            """
            latest_mock_test = ask_gemini(prompt)
            mock_test = latest_mock_test
            result = ""
            
           elif action == "evaluate_mock":

            student_answer = request.form.get("student_answer", "")
            question_paper = request.form.get("mock_test_data", "")
            prompt = f"""
            You are an experienced CBSE/RBSE/State Board examiner.

            Below is the original question paper.

            ===========================
            QUESTION PAPER
            ===========================

            {question_paper}

            ===========================
            STUDENT ANSWER
            ===========================

            {student_answer}

            Evaluate according to board marking scheme.
            Evaluate exactly like a CBSE/RBSE/State Board examiner.

            Marks should always be awarded out of the TOTAL marks of the paper.

            If some questions are not attempted, award zero marks for those questions.

            Do not convert the score based only on attempted questions.

            After the score, also mention:

            📌 Attempt Status

            ✔ Attempted: __ Questions

            ❌ Not Attempted: __ Questions
            
            Give output in this format only:

            📊 Evaluation Report

            ⭐ Score: __ / Total Marks
            
            📌 Attempt Status

            ✔ Attempted: __ Questions

            ❌ Not Attempted: __ Questions

            ✅ Strong Points

            ❌ Mistakes

            📚 Model Answer

            💡 Improvement Tips

            Keep feedback encouraging.
            """

            result = ask_gemini(prompt) 
           
           elif action == "solve_question":

            prompt = f"""
            You are India's best school teacher.

            Student Class: {student_class}
            Subject: {subject}

            Topic / Question:
            {notes}

            Your job is NOT just to solve the question.

            Teach the student while solving.

            Follow these rules:

            If the subject is Mathematics, Physics, Chemistry, Accountancy, Economics or Computer Science:

            1. Explain the concept first.
            2. Tell why this concept is important.
            3. Solve step by step.
            4. Explain every step.
            5. Highlight important formulas.
            6. Give shortcut/trick if possible.
            7. Tell common mistakes students make.
            8. Give one extra practice question.
            9. Give the final answer.

            Language Rules:

            - Use very simple English.
            - Explain like a friendly school teacher.
            - Use headings.
            - Never skip steps.
            - Keep answers neat.
            - Make learning easy instead of only giving the answer.
            """
            result = ask_gemini(prompt)
           elif action == "story_mode":
            print("INSIDE STORY MODE")   
            story_count += 1
            prompt = f"""
            Explain this topic as an interactive story-based learning game.
            Class: {student_class}
            Subject: {subject}

            Topic/Notes:
            {notes}

            Rules:
            - Use natural Hinglish (Hindi + English mixed).
            - Talk like a friendly teacher and student conversation.
            - Make learning fun and engaging.
            - Use characters, situations, and adventures.
            - Explain all concepts accurately.
            - Use simple language suitable for school and college students.
            - Add emojis where appropriate.
            - Ask small questions during the story to keep students involved.
            - Give choices like A/B options when possible.
            - Relate concepts to real-life examples.
            - End with a short quiz and answers.
            - Avoid very formal Hindi and difficult vocabulary.
         
            Use Story Learning ONLY for these subjects:

            - History
            - Geography
            - Political Science
            - Biology
            - English Literature
            - EVS
            - Business Studies

            If the selected subject is NOT in this list, DO NOT create a story.

            Instead politely tell the student:

            "This subject is better learned using the Solve Question feature because it contains formulas, calculations or logical problem solving."
            Output Format:
            🎮 Story Title

            👨‍🏫 Teacher

            👦 Student

            📖 Story Begins

            💡 Learn the Concept

            🎯 Small Activity

            🧠 Did You Understand?

            🏆 Mini Quiz

            ✅ Answers
            """
            result = ask_gemini(prompt)
            print("STORY RESULT =", result)
           
           elif action == "Board Exam Coach":

            prompt = f"""
            You are India's best Board Exam Coach for school students.

            Student Details:
            Class: {student_class}
            Subject: {subject}

            Topic:
            {notes}

            Create a professional Board Exam Guide using Markdown.

            Follow this exact format.

            # 🎯 Board Exam Coach

            ## 📚 Subject
            Mention class and subject.

            ---

            ## ⭐ Exam Strategy
            Give 5 short points.

            ---

            ## 📝 Answer Writing Tips

            ### ✅ 2 Marks
            - 2-3 points only

            ### ✅ 3 Marks
            - 3-4 points only

            ### ✅ 5 Marks
            - Introduction
            - Main Body
            - Conclusion

            ---

            ## 📌 Most Important Topics
            Mention 5 important topics for revision.

            ---

            ## 🔑 Important Keywords
            Give 10 important keywords.

            ---

            ## ❌ Common Mistakes
            Give only 5 points.

            ---

            ## 💡 Examiner Secret Tips
            Give 5 practical examiner tips.

            ---

            ## 🏆 Scoring Strategy
            Explain how to score above 90%.

            ---

            ## ⏰ Last Day Revision Plan

            🌅 Morning

            ☀ Afternoon

            🌇 Evening

            🌙 Night

            Mention what to revise in each session.

            ---

            ## 🎯 Predicted Board Questions
            Generate 5 most expected board exam questions from this topic.

            ---

            ## 🚀 Motivation
            End with a short motivational message.

            Rules:
            - Keep every section short.
            - Use emojis.
            - Use bullet points.
            - Don't write long paragraphs.
            - Make it visually attractive.
            Use simple Hinglish.
            """
            result = ask_gemini(prompt) 
           elif action == "exam_tips":

            prompt = f"""
            Give exam preparation tips for:
            Class: {student_class}
            Subject: {subject}

            Topic:
            {notes}

            Include:

            1. Important Keywords
            2. Common Mistakes
            3. Presentation Tips
            4. Examiner Expectations
            5. Last Day Revision Tips
            6. Scoring Strategy

            Use simple Hinglish.
            """

            result = ask_gemini(prompt) 
           elif action == "image_solver":

            if image and image.filename != "":

                filename = secure_filename(image.filename)

                filepath = os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )

                image.save(filepath)

                result = f"""
           Image uploaded successfully!

           Image Path:
           {filepath}

           Next  Step:
           OCR integration pending.
           Soon AI will read the image and solve the question automatically.
            """
            else:
                    result = "⚠️ Please upload an image first." 
# Badge Logic

    badge = "🌱 Beginner"

    if quiz_count >= 5:
     badge = "🎯 Test Warrior"

    if story_count >= 10:
     badge = "📚 Story Master"
 
    xp = (
        story_count * 20
        + quiz_count * 30
        + studyplan_count * 15
)

    level = (xp // 100) + 1

    xp_percent = xp % 100

    if  xp_percent == 0 and xp > 0:
        xp_percent = 100
    
    print("FINAL RESULT =", result)  
         
    return render_template(
        "index.html",
        result=result,
        subject=subject,
        student_class=student_class,
        student_type=student_type,
        quiz_count=quiz_count,
        summary_count=summary_count,
        studyplan_count=studyplan_count,
        story_count=story_count,
        mock_test=mock_test,
        badge=badge,
        xp=xp,
        level=level,
        xp_percent=xp_percent, 
        
        
    )        
if __name__ == "__main__":
    app.run(debug=True)