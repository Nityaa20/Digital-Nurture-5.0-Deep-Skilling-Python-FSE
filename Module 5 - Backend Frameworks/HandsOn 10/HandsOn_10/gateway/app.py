"""
====================================================================
 Digital Nurture 5.0 - Python Backend Frameworks
 HANDS-ON 10 [Advanced] - Microservices Architecture
 SERVICE: API Gateway  (runs on port 5000)
====================================================================

WHO THIS IS FOR:
Written for a beginner / fresher.

WHAT IS AN API GATEWAY?
   Instead of your frontend app needing to know "courses live at
   port 5001, students live at port 5002, auth lives somewhere
   else...", it talks to ONE address (the Gateway), and the Gateway
   figures out which backend service should actually handle each
   request, then forwards ("proxies") the request there and sends
   the response back.

   Routing rules for THIS gateway:
       /api/courses/*   -> Course Service  (port 5001)
       /api/students/*  -> Student Service (port 5002)

   NOTE (important, honest disclaimer): a real production API
   Gateway (like Kong, AWS API Gateway, or NGINX) ALSO handles
   authentication, rate limiting, SSL/TLS termination, request
   logging, and more. This file only demonstrates the core ROUTING
   concept in the simplest way possible - it is a teaching example,
   not something you'd deploy as-is.

HOW TO RUN (3 terminals needed):
    Terminal 1: cd course_service  && python app.py   (port 5001)
    Terminal 2: cd student_service && python app.py   (port 5002)
    Terminal 3: cd gateway         && python app.py   (port 5000)

    pip install flask requests   (needed in all three services)
====================================================================
"""

from flask import Flask, request, Response
import requests

app = Flask(__name__)

# --------------------------------------------------------------
# Where each backend service actually lives. The Gateway is the
# ONLY thing that needs to know these addresses - the outside
# world (your frontend, Postman, etc.) only ever talks to the
# Gateway on port 5000.
# --------------------------------------------------------------
SERVICE_MAP = {
    "courses": "http://127.0.0.1:5001",
    "students": "http://127.0.0.1:5002",
}


def proxy_request(target_base_url: str, path: str):
    """
    Forward whatever request the client sent (method, body, query
    string) to the real service, then return whatever that service
    replied with, unchanged, back to the client.

    This is the heart of the "reverse proxy" pattern.
    """
    target_url = f"{target_base_url}/{path}"

    try:
        upstream_response = requests.request(
            method=request.method,
            url=target_url,
            headers={k: v for k, v in request.headers if k.lower() != "host"},
            params=request.args,
            data=request.get_data(),
            timeout=5,
        )
    except requests.exceptions.ConnectionError:
        # The backend service this route points to is down.
        return {"error": f"Upstream service for '{target_url}' is unavailable"}, 503

    # Forward the upstream status code, body, and content-type back
    # to whoever called the Gateway - the client should not be able
    # to tell the difference between calling the Gateway directly vs
    # calling the real service directly (other than the URL).
    return Response(
        upstream_response.content,
        status=upstream_response.status_code,
        content_type=upstream_response.headers.get("Content-Type", "application/json"),
    )


@app.route("/api/courses/", defaults={"subpath": ""}, methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
@app.route("/api/courses/<path:subpath>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def route_to_course_service(subpath):
    """Any request starting with /api/courses/... goes to Course Service."""
    return proxy_request(SERVICE_MAP["courses"], f"api/courses/{subpath}")


@app.route("/api/students/", defaults={"subpath": ""}, methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
@app.route("/api/students/<path:subpath>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def route_to_student_service(subpath):
    """Any request starting with /api/students/... goes to Student Service."""
    return proxy_request(SERVICE_MAP["students"], f"api/students/{subpath}")


@app.route("/", methods=["GET"])
def health_check():
    return {"service": "api_gateway", "status": "running", "port": 5000,
            "routes": {"courses": SERVICE_MAP["courses"], "students": SERVICE_MAP["students"]}}, 200


if __name__ == "__main__":
    app.run(port=5000, debug=True)
