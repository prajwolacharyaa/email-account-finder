"""Flask web app for account_finder."""

from __future__ import annotations

from dataclasses import asdict

from flask import Flask, jsonify, render_template, request, send_file

from scanner import export_csv, export_pdf, load_history, scan_email


app = Flask(__name__)


@app.route("/")
def index():
    """Render the main UI."""
    return render_template("index.html")


@app.post("/api/scan")
def api_scan():
    """Scan one email address and return JSON results."""
    payload = request.get_json(silent=True) or {}
    email = payload.get("email", "")

    try:
        results = scan_email(email)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({"email": email.strip().lower(), "results": [asdict(result) for result in results]})


@app.get("/api/history")
def api_history():
    """Return recent searches saved on this machine."""
    return jsonify(load_history())


@app.post("/api/export/<file_type>")
def api_export(file_type: str):
    """Export fresh scan results as CSV or PDF."""
    payload = request.get_json(silent=True) or {}
    email = payload.get("email", "")

    try:
        results = scan_email(email)
        if file_type == "csv":
            path = export_csv(email, results)
            return send_file(path, as_attachment=True)
        if file_type == "pdf":
            path = export_pdf(email, results)
            return send_file(path, as_attachment=True)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 500

    return jsonify({"error": "Unsupported export type."}), 400


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
