from flask import Blueprint, render_template, request
from .services import qa_chain # Assuming services.py holds the logic

bp = Blueprint('main', __name__)

@bp.route("/", methods=["GET", "POST"])
def index():
    answer = None
    sources = None
    query = ""
    if request.method == "POST":
        query = request.form["query"]
        if query:
            response = qa_chain.invoke({"query": query})
            answer = response["result"]
            sources = "\n".join([doc.metadata.get("source", "Unknown Source") for doc in response["source_documents"]])
    return render_template("index.html", answer=answer, sources=sources, query=query)

