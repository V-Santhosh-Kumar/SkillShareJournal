from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("feeds.html")

@app.route('/<page>')
def image(page):
    return render_template(f"{page}.html")

if __name__ == "__main__":
    app.run(debug=True)