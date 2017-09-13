"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/")
def show_homepage():
  """Show homepage"""

  students = hackbright.get_all_students()

  projects = hackbright.get_all_projects()

  return render_template("hackbright_home.html",
                         students=students,
                         projects=projects)


@app.route("/student/<github>")
def get_student(github):
    """Show information about a student."""

    first, last, github = hackbright.get_student_by_github(github)

    projects = hackbright.get_grades_by_github(github)

    # return "{acct} is the GitHub account for {first} {last}".format(
    #     acct=github, first=first, last=last)
    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           projects=projects)
    return html


@app.route("/student-search")
def get_student_form():
    """Show form for searching a student."""

    return render_template("student_search.html")


@app.route("/student-add", methods=['GET'])
def show_add_student_form():
    return render_template("add_student.html")


@app.route("/student-added", methods=['POST'])
def add_student():
    """Add a student"""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')


    hackbright.make_new_student(first_name, last_name, github)



    return render_template("student_added.html",
                           first=first_name,
                           last=last_name,
                           github=github)


@app.route("/project/<project_name>")
def show_project_info(project_name):
    """Shows project title, max grade and description"""

    # title =
    projects = hackbright.get_project_by_title(project_name)

    grades_list = hackbright.get_grades_by_title(project_name)

    return render_template("project-detail.html",
                           projects=projects,
                           grades_list=grades_list)



if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
