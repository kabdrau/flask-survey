from flask import Flask, request, render_template,  redirect, flash,  jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES = []
ALL_RESPONSES = {}


@app.route('/')
def home_page():
    """Shows home page"""
    title = survey.title
    instruction = survey.instructions
    
    return render_template('home.html', title=title, instruction=instruction)


@app.route('/question/<int:id>')
def question(id):
    """Questions"""
    # handling nonexisting question id
    if (id > len(survey.questions)):
        flash("Question doesn't exist", 'error')
        return redirect(f"/question/{len(RESPONSES)}")

    question = survey.questions[id].question
    choices = survey.questions[id].choices

    # follow QA order
    if (id != len(RESPONSES)):
        flash('Invalid question id', 'error')
        return redirect(f"/question/{len(RESPONSES)}")

    return render_template("question.html", question=question, choices=choices, id=id, responses=RESPONSES)


@app.route('/answer', methods=["POST"])
def answer():
    # get the response choice
    choice = request.form.get('answer')

    # handle choice = None
    if choice is None:
        flash('Please answer the question', 'error')
        return redirect(f"/question/{len(RESPONSES)}")

    # add this choice to responses
    RESPONSES.append(choice)
    if (len(RESPONSES) < len(survey.questions)):
        # redirect to the next question if any
        return redirect(f"/question/{len(RESPONSES)}")
    else:
        # if answered all questions, save answers and redirect to completion page
        ALL_RESPONSES[len(ALL_RESPONSES)] = RESPONSES.copy()
        RESPONSES.clear()
        return redirect("/complete")


@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""
    flash('All questions answered', 'success')

    return render_template("completion.html")