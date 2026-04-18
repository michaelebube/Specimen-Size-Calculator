from __future__ import annotations

from flask import Flask, jsonify, redirect, render_template, request, url_for

from core import fetch_records, store_record

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    message_type = ""

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        microscope_size = request.form.get("microscope_size", "").strip()
        magnification = request.form.get("magnification", "").strip()
        unit = request.form.get("unit", "um").strip() or "um"

        try:
            _, actual_size = store_record(
                username, float(microscope_size), float(magnification), unit
            )
            message = f"Saved. Actual size = {actual_size:.6f} {unit}"
            message_type = "success"
            return redirect(url_for("index", msg=message, mt=message_type))
        except ValueError as exc:
            message = str(exc)
            message_type = "error"

    if request.method == "GET":
        message = request.args.get("msg", "")
        message_type = request.args.get("mt", "")

    rows = fetch_records(limit=200)
    return render_template(
        "index.html", records=rows, message=message, message_type=message_type
    )


@app.get("/api/records")
def api_records():
    rows = fetch_records(limit=200)
    payload = [
        {
            "id": row["id"],
            "username": row["username"],
            "microscope_size": row["microscope_size"],
            "magnification": row["magnification"],
            "actual_size": row["actual_size"],
            "unit": row["unit"],
            "created_at": row["created_at"],
        }
        for row in rows
    ]
    return jsonify(payload)


if __name__ == "__main__":
    app.run(debug=True)
