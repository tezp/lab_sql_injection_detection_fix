from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, request

from database import get_connection

app = Flask(__name__)

LOG_PATH = Path(__file__).resolve().parents[1] / "logs" / "app.log"


def write_log(message: str) -> None:
    LOG_PATH.parent.mkdir(exist_ok=True)

    with open(LOG_PATH, "a", encoding="utf-8") as log_file:
        log_file.write(f"{datetime.utcnow().isoformat()} {message}\n")


@app.route("/", methods=["GET"])
def health_check():
    return jsonify(
        {
            "status": "running",
            "message": "Globomantics Employee Portal API"
        }
    )


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    username = data.get("username", "")
    password = data.get("password", "")

    write_log(f"LOGIN_ATTEMPT username={username} password={password}")

    connection = get_connection()
    cursor = connection.cursor()

    # Vulnerable query for lab demonstration.
    # query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    query = f"""
    SELECT *
    FROM users
    WHERE username='{username}'
    AND password='{password}'
    """

    cursor.execute(query)

    write_log(f"QUERY_EXECUTED {query}")

    try:
        cursor.execute(query)
        user = cursor.fetchone()
    except Exception as error:
        connection.close()
        write_log(f"QUERY_ERROR error={str(error)}")
        return jsonify({"status": "error", "message": "Query execution failed"}), 500

    connection.close()

    if user:
        write_log(f"LOGIN_SUCCESS username={username}")
        return jsonify(
            {
                "status": "success",
                "user": user[1],
                "role": user[3]
            }
        )

    write_log(f"LOGIN_FAILED username={username}")
    return jsonify({"status": "failed"}), 401


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)