import os
from flask import Flask, request, render_template, jsonify # type: ignore
from rich.console import Console # type: ignore
from rich.panel import Panel # type: ignore
from werkzeug.utils import secure_filename # type: ignore
from debugger import analyze_code
from llm_debugger import get_suggestions


app = Flask(__name__)
console = Console()

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"py"}  # Only allow Python files

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure upload folder exists

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Only .py files are allowed"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    console.log(Panel.fit(f"[bold blue]Uploaded File:[/bold blue] {filename}"))

    # Read file content
    with open(file_path, "r") as f:
        source_code = f.read()

    # Step 1: Analyze code for issues
    issues = analyze_code(source_code)
    ai_suggestions = []

    if issues:
        for issue in issues:
            suggestion = get_suggestions(issue, source_code)
            ai_suggestions.append({"issue": issue, "suggestion": suggestion})

    response = {
        "issues_detected": issues,
        "ai_suggestions": ai_suggestions
    }

    console.log(Panel.fit(f"[bold green]Response Sent:[/bold green]\n{response}"))

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)