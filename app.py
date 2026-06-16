import logging
import os
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template_string, request


VALID_USERNAME = os.environ.get("LOGIN_USERNAME", "admin")
VALID_PASSWORD = os.environ.get("LOGIN_PASSWORD", "password123")


def create_app():
    app = Flask(__name__)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    @app.get("/")
    def index():
        return jsonify(
            {
                "message": "Flask login monitoring demo",
                "login_endpoint": "/login",
            }
        )

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "GET":
            return render_template_string(
                """
                <!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <title>Login</title>
                    <style>
                      body {
                        font-family: Arial, sans-serif;
                        max-width: 420px;
                        margin: 48px auto;
                        padding: 0 16px;
                      }
                      label, input, button {
                        display: block;
                        width: 100%;
                        box-sizing: border-box;
                      }
                      label {
                        margin-top: 16px;
                        font-weight: 700;
                      }
                      input, button {
                        margin-top: 8px;
                        padding: 10px;
                        font-size: 16px;
                      }
                      button {
                        margin-top: 20px;
                        cursor: pointer;
                      }
                    </style>
                  </head>
                  <body>
                    <h1>Login</h1>
                    <form method="post" action="/login">
                      <label for="username">Username</label>
                      <input id="username" name="username" required>

                      <label for="password">Password</label>
                      <input id="password" name="password" type="password" required>

                      <button type="submit">Log in</button>
                    </form>
                  </body>
                </html>
                """
            )

        payload = request.get_json(silent=True) or request.form
        username = payload.get("username", "")
        password = payload.get("password", "")
        client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        timestamp = datetime.now(timezone.utc).isoformat()

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            app.logger.info(
                "LOGIN_SUCCESS username=%s ip=%s timestamp=%s",
                username,
                client_ip,
                timestamp,
            )
            if request.is_json:
                return jsonify({"message": "Login successful"}), 200

            return "Login successful", 200

        app.logger.warning(
            "LOGIN_FAILED username=%s ip=%s timestamp=%s",
            username,
            client_ip,
            timestamp,
        )
        if request.is_json:
            return jsonify({"message": "Invalid username or password"}), 401

        return "Invalid username or password", 401

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
