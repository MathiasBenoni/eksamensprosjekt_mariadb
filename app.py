from flask import Flask, render_template, request, redirect, url_for, flash
from mariadb_python import get_adjectives, write
from wordcloud_python import make_cloud
import markdown
import time
from pathlib import Path

app = Flask(__name__)
app.secret_key = "test"

_DOCS_DIR = Path(__file__).parent / "documents"

def _load_doc(filename):
    return markdown.markdown(_DOCS_DIR.joinpath(filename).read_text(encoding="utf-8"), extensions=["extra"])

@app.route("/", methods=["GET"])
def index():
    adjectives = get_adjectives()
    has_cloud = make_cloud(adjectives) != "NOPE"
    wordcloud = {
        "light": url_for("static", filename="images/cloud_light.png"),
        "dark":  url_for("static", filename="images/cloud_dark.png"),
        "ts":    int(time.time()),
    } if has_cloud else None
    return render_template(
        "index.html",
        wordcloud=wordcloud,
        privacy_html=_load_doc("privacy_policy.md"),
        terms_html=_load_doc("terms_of_use.md"),
        manual_html=_load_doc("user_manual.md"),
    )

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
 