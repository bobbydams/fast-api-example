import os

from flask import Blueprint, render_template, request, redirect

from apps.demo.context import Context

bp = Blueprint("demo", __name__, url_prefix="/demo")
bp.template_folder = os.path.join(os.path.dirname(__file__), "templates")
context = Context()


@bp.route("", methods=["GET"])
def index():
    return redirect("demo/books"), 302


@bp.route("/books", methods=["GET", "POST"])
def books():
    response = {}
    if request.method == "POST":
        if request.form.get("get_by_title"):
            response = context.book_service.get(
                request.form["get_by_title"],
            )
        else:
            response = context.book_service.add(
                request.form["title"],
                request.form["author"],
                request.form["publisher"],
                int(request.form["pages"]),
            )

    return render_template("/index.html", response=response)
