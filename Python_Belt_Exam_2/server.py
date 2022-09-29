import re
from flask import Flask, render_template, request, redirect, session, flash
from mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.secret_key = 'secret'
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


@app.route('/')
def begin():
    return render_template("login.html")


@app.route('/adduser', methods=['POST'])
def register():
    is_valid = True
    print(request.form)

    if len(request.form['first_name']) < 2:
        is_valid = False
        flash("Please enter your first name")

    if len(request.form['last_name']) < 2:
        is_valid = False
        flash("Please enter your last name")

    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Invalid email, please retry")

    else:
        mysql = connectToMySQL("belt_exam_retake")
        query = "SELECT * FROM users WHERE email = %(email)s"
        data = {
            "email": request.form["email"]
        }
        result = mysql.query_db(query, data)
        if len(result) > 0:
            flash("Email already exists")
            is_valid = False

    if len(request.form['password']) < 8:
        is_valid = False
        flash("Please enter a password at least 8 characters long")

    if request.form['password'] != request.form['confirm']:
        is_valid = False
        flash("Passwords must be the same")
    mysql = connectToMySQL("belt_exam_retake")
    query = "SELECT * FROM users WHERE email= %(email)s;"
    data = {
        "email": request.form["email"],
    }
    result = mysql.query_db(query, data)
    if len(result) > 0:
        is_valid = False
        flash("Email already in use")
    if not is_valid:
        return redirect("/")

    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        mysql = connectToMySQL("belt_exam_retake")
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password_hash)s);"
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form["email"],
            "password_hash": pw_hash,
        }
        newuser = mysql.query_db(query, data)
        session['username'] = newuser
        print(newuser)
        flash("You have registered!")
        flash('please log in!')
        return redirect('/')


@app.route('/login', methods=["POST"])
def login():
    is_valid = True
    

    if len(request.form["email"]) < 1:
        flash("incomplete email, please re-enter")
        is_valid = False
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid email address!")
        is_valid = False
    else:
        mysql = connectToMySQL("belt_exam_retake")
        query = "SELECT * FROM users WHERE email = %(email)s"
        data = {
            "email": request.form["email"]
        }
        result = mysql.query_db(query, data)
        print(result)
    if len(result) > 0:
        flash("Account already created for this email")
    if is_valid == False:
        return redirect("/")
    mysql = connectToMySQL("belt_exam_retake")
    query = "SELECT * FROM users WHERE email = %(email)s;"
    data = {"email": request.form["email"]}
    result = mysql.query_db(query, data)
    if len(result) > 0:
        if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
            session['userid'] = result[0]['id']
            session['username'] = result[0]['first_name']
            return redirect('/welcome')
        else:
            flash("Login Failed")
            return redirect('/')
    else:
        flash("Please provide valid login")
        return redirect('/')


@app.route("/welcome", methods = ["GET"])
def render_magazines():
    mysql = connectToMySQL("belt_exam_retake")
    query = ('SELECT * FROM users WHERE id = (%(users_id)s);')
    data = {
        "users_id":session["userid"]
    }
    user = mysql.query_db(query, data)
    mysql = connectToMySQL("belt_exam_retake")
    magazines = mysql.query_db(
        "SELECT * FROM magazines JOIN users WHERE users.id = magazines.users_id;")
    return render_template("welcome.html", users=user, magazines=magazines)


@app.route("/view/<magazines_id>")
def show(magazines_id):
    mysql = connectToMySQL("belt_exam_retake")
    query = "SELECT * FROM magazines JOIN users on users.id= users_id WHERE magazines.id= %(magazines_id)s;"
    data = {
        "magazines_id": magazines_id
    }
    magazines = mysql.query_db(query, data)
    print(magazines)
    return render_template("view.html", magazines=magazines)


@app.route("/edit/<users_id>")
def edit_user(users_id):
    mysql = connectToMySQL("belt_exam_retake")
    query = "SELECT * FROM users WHERE id = (%(users_id)s);"
    data = {
        "users_id": users_id
    }
    users = mysql.query_db(query, data)
    print(users)
    mysql = connectToMySQL("belt_exam_retake")
    query = "SELECT * FROM magazines JOIN users on users.id = users_id WHERE users.id = %(magazines.users_id)s;"
    data = {
        "magazines.users_id": users_id
    }
    magazines = mysql.query_db(query, data)
    print(magazines)
    return render_template("edit.html", users=users, magazines=magazines)


@app.route("/updated/<users_id>", methods=['POST'])
def edit(users_id):
    is_valid = True
    if len(request.form['first_name']) < 2:
        is_valid = False
        flash("Please enter your first name")
    if len(request.form['last_name']) < 2:
        is_valid = False
        flash("Please enter your last name")
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Invalid email!")
    if not is_valid:
        return redirect("/edit/%s" % users_id)
    else:
        mysql = connectToMySQL("belt_exam_retake")
        query = ("UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = (%(users_id)s);")
        data = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "users_id": users_id
        }
        mysql.query_db(query, data)
        flash("User Updated")
        return redirect("/welcome")


@app.route('/addnew')
def write_new():
    return render_template('new.html')


@app.route("/new_magazine", methods=['POST'])
def add_new():
    is_valid= True
    if len(request.form['name']) < 2:
        is_valid = False
        flash("Please enter a title")
    if len(request.form['description']) < 2:
        is_valid = False
        flash("Please enter the description")
    if not is_valid:
        return redirect("/addnew")
    mysql = connectToMySQL("belt_exam_retake")
    query = "INSERT INTO magazines (name, description, users_id) VALUES (%(name)s, %(description)s, %(users_id)s);"
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "users_id": session['users_id']
    }
    mysql.query_db(query, data)
    return redirect('/welcome')


@app.route('/delete/<magazine_id>', methods=['POST'])
def delete(magazine_id):
    mysql = connectToMySQL("belt_exam_retake")
    query = "DELETE FROM magazines WHERE id= %(magazine_id)s;"
    data = {
        "magazine_id": magazine_id,
    }
    mysql.query_db(query, data)
    return redirect("/welcome")


@app.route('/logout', methods=["POST"])
def logout():
    session.clear()
    return render_template("logout.html")


if __name__ == "__main__":
    app.run(debug=True)
