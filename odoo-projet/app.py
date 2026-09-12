from flask import Flask, jsonify, request, render_template, send_from_directory
from connexion import get_stock, get_sales, get_invoices
from agent import ask_agent

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/stock")
def stock():
    return jsonify(get_stock(limit=20))


@app.route("/api/sales")
def sales():
    return jsonify(get_sales(limit=20))


@app.route("/api/invoices")
def invoices():
    return jsonify(get_invoices(limit=20))


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    question = (data or {}).get("question", "")
    if not question.strip():
        return jsonify({"answer": "Pose-moi une question."})
    answer = ask_agent(question)
    return jsonify({"answer": answer})


@app.route("/rapports/<path:filename>")
def rapports(filename):
    return send_from_directory("rapports", filename)


if __name__ == "__main__":
    app.run(debug=True)
