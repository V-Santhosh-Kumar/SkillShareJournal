from flask import Flask, render_template
from mongoengine import connect, connection

app = Flask(__name__)

app.secret_key = "supersecret123"

try:
    connect(host="mongodb://localhost:27017/skillShareJournal")
    if connection.get_connection():
        print("Database Connected Successfully.")
    else:
        print("Database not Connected.")
except Exception as e:
    print("Error: ", str(e))

from roles import role_bp
app.register_blueprint(role_bp)

from auth import auth_bp
app.register_blueprint(auth_bp)

from comment import comment_bp
app.register_blueprint(comment_bp)

from like import like_bp
app.register_blueprint(like_bp)

from note import note_bp
app.register_blueprint(note_bp)

from savednotes import savednotes_bp
app.register_blueprint(savednotes_bp)

from tags import tags_bp
app.register_blueprint(tags_bp)

from user import user_bp
app.register_blueprint(user_bp)

@app.route('/')
def main():
    return render_template("feeds.html")

@app.route('/<page>')
def image(page):
    return render_template(f"{page}.html")

if __name__ == "__main__":
    app.run(debug=True)