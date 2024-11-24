from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/run-script", methods=["POST"])
def run_script():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    script_result = my_script_logic(data.get("input"))

    return jsonify({"result": script_result})


def my_script_logic(input_value):
    return f"Processed input: {input_value}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
