from flask import Flask, render_template, request, redirect, url_for, flash
from mariadb_python import get_adjectives, write

app = Flask(__name__)
app.secret_key = "test"

@app.route("/", methods=["GET"])
def index():
    adjectives = get_adjectives()
    return render_template("index.html", adjectives=adjectives)

@app.route("/", methods=["POST"])
def add():
    word = request.form.get("word", "").strip().lower()
    if not word:
        flash("Empty input!", "error")
        return redirect(url_for("index"))

    write(word)
    flash(f'"{word}" added!', "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
 