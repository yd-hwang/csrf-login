from flask import Flask, request, render_template_string, session, redirect, url_for
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# --- 템플릿 HTML들 ---
login_page = """
<!doctype html>
<html>
<head><title>Login</title>
<style>
    body { font-family: Arial; margin: 50px; }
    form { max-width: 300px; margin: auto; padding: 20px; border: 1px solid #ccc; border-radius: 8px; }
    input { width: 100%; padding: 8px; margin: 6px 0; }
    button { width: 100%; padding: 10px; background-color: #007BFF; color: white; border: none; }
</style>
</head>
<body>
<h2 style="text-align:center;">🔐 CSRF Login</h2>
<form method="POST" action="/login">
  <input type="text" name="username" placeholder="Username" required><br>
  <input type="password" name="password" placeholder="Password" required><br>
  <input type="hidden" name="csrf_token" value="{{ csrf }}">
  <button type="submit">Login</button>
</form>
</body>
</html>
"""

success_page = """
<!doctype html>
<html>
<head><title>Success</title></head>
<body style="font-family: Arial; margin: 50px;">
    <h2>🎉 Welcome, {{ username }}!</h2>
    <p>You have successfully logged in.</p>
    <p><a href="/profile">Go to Profile Page →</a></p>
    <form method="POST" action="/logout">
        <button>Log out</button>
    </form>
</body>
</html>
"""

profile_page = """
<!doctype html>
<html>
<head><title>Profile</title>
<style>
    body { font-family: 'Segoe UI', sans-serif; margin: 50px; }
    .card { max-width: 400px; margin: auto; padding: 20px; border: 1px solid #ddd; border-radius: 12px; background-color: #f9f9f9; }
    h2 { color: #2c3e50; }
    .info { margin: 10px 0; }
</style>
</head>
<body>
<div class="card">
    <h2>👤 Profile</h2>
    <div class="info"><strong>Name:</strong> Ha-eun Kim</div>
    <div class="info"><strong>Age:</strong> 24</div>
    <div class="info"><strong>Occupation:</strong> UX Designer</div>
    <div class="info"><strong>Location:</strong> Seoul, South Korea</div>
    <div class="info"><strong>About:</strong> A passionate and creative 20-something who loves turning complex ideas into elegant designs. Always curious, always learning.</div>
</div>
</body>
</html>
"""

# --- 라우팅 ---
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
            return "<h3>🚨 CSRF Token Invalid!</h3>", 403

        if username == "admin" and password == "1234":
            session["username"] = username
            return redirect(url_for("success"))
        else:
            return "<h3>❌ Invalid credentials.</h3>", 401

    csrf = secrets.token_hex(16)
    session["csrf_token"] = csrf
    return render_template_string(login_page, csrf=csrf)

@app.route("/success")
def success():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template_string(success_page, username=session["username"])

@app.route("/profile")
def profile():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template_string(profile_page)

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
