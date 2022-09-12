from flask import Flask, request, render_template,  redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = "qwerty123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    """Show home page."""
    title = survey.title
    instruction = survey.instructions
    
    return render_template('home.html', title=title, instruction=instruction)

@app.route('/start', methods=["POST"])
def start_session():
    """Clear session of responses."""
    session['responses'] = []

    return redirect('/question/0')


@app.route('/question/<int:id>')
def question(id):
    """Display current question.""" 

    # get responses from the session
    responses = session.get('responses')

    # handling nonexisting question id
    if (id > len(survey.questions)):
        flash("Question doesn't exist", 'error')
        return redirect(f"/question/{len(responses)}")

    question = survey.questions[id].question
    choices = survey.questions[id].choices

    # follow QA order
    if (id != len(responses)):
        flash('Invalid question id', 'error')
        return redirect(f"/question/{len(responses)}")

    return render_template("question.html", question=question, choices=choices, id=id)


@app.route('/answer', methods=["POST"])
def answer():
    """Handle answers."""
    # get responses from the session and choice from the form
    responses = session.get('responses')
    choice = request.form.get('answer')

    # handle None choice
    if choice is None:
        flash('Please answer the question', 'error')
        return redirect(f"/question/{len(responses)}")

    # add this response to the session
    responses.append(choice)
    session['responses'] = responses
    
    # if answered all questions redirect to completion page
    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    else:
        # redirect to the next question if any
        return redirect(f"/question/{len(responses)}")


@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""
    flash('All questions answered', 'success')

    return render_template("completion.html")