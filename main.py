from flask import Flask, request, render_template_string, session, redirect, url_for
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

login_form = """
<!doctype html>
<title>Login</title>
<h2>CSRF Login Form</h2>
<form method="POST" action="/login">
  <input type="text" name="username" placeholder="Username"><br>
  <input type="password" name="password" placeholder="Password"><br>
  <input type="hidden" name="csrf_token" value="{{ csrf }}">
  <button type="submit">Login</button>
</form>
"""

profile_page = """
<!doctype html>
<title>Profile</title>
<h2>Welcome, {{ username }}!</h2>
<p>You are now logged in.</p>
<form method="POST" action="/logout">
  <button type="submit">Log out</button>
</form>
"""

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        token = request.form.get("csrf_token")
        if token != session.get("csrf_token"):
            return "<h3>CSRF Token Invalid!</h3>", 403
        if username == "admin" and password == "1234":
            session["username"] = username
            return redirect(url_for("profile"))
        else:
            return "<h3>Invalid username or password.</h3>", 401
    csrf = secrets.token_hex(16)
    session["csrf_token"] = csrf
    return render_template_string(login_form, csrf=csrf)

@app.route("/profile")
def profile():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template_string(profile_page, username=session["username"])

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
