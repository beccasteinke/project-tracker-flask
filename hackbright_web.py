"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, flash, session, redirect

import hackbright

app = Flask(__name__)
app.secret_key = 'ABC'

@app.route("/")
def index():
    return render_template('student_search.html')

@app.route("/student-add")
def student_add():
    """Add a student."""
    return render_template('student_add.html')


@app.route("/student-addinfo", methods=['POST'])
def student_addinfo():
    first = request.form.get('first')
    last = request.form.get('last')
    github = request.form.get('github')
    # print(first, last, github)
    hackbright.make_new_student(first, last, github)
    # print('Student successfully added')

    return render_template("student_info.html", first=first, last=last, github=github)

@app.route("/student")
def get_student():
    """Show information about a student."""
    github = request.args.get("github")

    first, last, github = hackbright.get_student_by_github(github)
    rows = hackbright.get_grades_by_github(github)

    return render_template("student_info.html", first=first, last=last, github=github, rows=rows)

@app.route("/project")
def get_project():
    """Show information about a project."""
    project_title = request.args.get("title")

    title, desc, max_grade = hackbright.get_project_by_title(project_title)
    return render_template("project_info.html", title=title, desc=desc, max_grade=max_grade)

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True, host="0.0.0.0")
