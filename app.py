"""Tiny Flask app — applied-ai-sandbox.

Each task in tasks/ asks you to add or fix one piece. The tests in tests/
describe exactly what "done" means.
"""
from __future__ import annotations

from flask import Flask, render_template, request, redirect, url_for, abort


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sandbox-not-a-real-secret"

    # In-memory store for the sandbox. Resets on every restart, which is
    # fine for practice. Real apps use a database.
    app.notes: list[dict] = []  # type: ignore[attr-defined]

    @app.route("/")
    def home():
        starred_only = request.args.get("starred") == "true"
        indexed_notes = [
            (idx, note) for idx, note in enumerate(app.notes)
            if not starred_only or note.get("starred")
        ]
        return render_template("home.html", notes=indexed_notes, starred_only=starred_only)

    @app.route("/notes/new", methods=["GET", "POST"])
    def new_note():
        if request.method == "POST":
            title = (request.form.get("title") or "").strip()
            body = (request.form.get("body") or "").strip()
            errors = {}
            if not title:
                errors["title"] = "Title is required"
            if not body:
                errors["body"] = "Body is required"
            if errors:
                return render_template("new_note.html", title=title, body=body, errors=errors)
            app.notes.append({"title": title, "body": body, "tags": [], "starred": False})
            return redirect(url_for("home"))
        return render_template("new_note.html")

    @app.route("/notes/<int:idx>/star", methods=["POST"])
    def star_note(idx):
        if idx < 0 or idx >= len(app.notes):
            abort(404)
        note = app.notes[idx]
        note["starred"] = not note.get("starred", False)
        return redirect(url_for("home"))

    @app.route("/notes/<int:idx>/delete", methods=["POST"])
    def delete_note(idx):
        if idx < 0 or idx >= len(app.notes):
            abort(404)
        app.notes.pop(idx)
        return redirect(url_for("home"))

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
