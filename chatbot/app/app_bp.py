from flask import Blueprint, render_template, request, jsonify
from flask.views import MethodView

bp = Blueprint("app", __name__, url_prefix="/")

@bp.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST":
        return jsonify({"response": "This is a POST request"})
    return render_template("chat.html")