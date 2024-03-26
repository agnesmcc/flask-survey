from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# responses = []

@app.route('/')
def home():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title=title, instructions=instructions)

@app.route('/start', methods=["POST"])
def start():
    session['responses'] = []
    return redirect('questions/0')

@app.route('/questions/<int:number>')
def questions(number):
    if number != len(session['responses']):
        # Prevent the user from going to a different question.
        flash('You are trying to access an invalid question!')
        return redirect("/questions/%s" % len(session['responses']))
    elif number >= len(satisfaction_survey.questions):
        # If all questions have been answered, then done.
        return redirect('/thank-you')
    # Return the rendered question page if more question need to be asked.
    question = satisfaction_survey.questions[number].question
    choices = satisfaction_survey.questions[number].choices
    return render_template('questions.html', number=number, question=question, choices=choices)

@app.route('/answer', methods=["POST"])
def answer():
    if len(session['responses']) >= len(satisfaction_survey.questions):
        return redirect('/thank-you')
    # If there are not enough responses, save the answer and 
    # move onto the next question.
    number = int(request.form.get('number'))
    answer = request.form.get('choice')
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses
    print(session['responses'])
    next_number = number + 1
    return redirect("/questions/%s" % next_number)

@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')