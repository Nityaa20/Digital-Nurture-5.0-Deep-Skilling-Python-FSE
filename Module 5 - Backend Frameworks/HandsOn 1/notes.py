"""
Handson 01 - Task 1: Request-Response Cycle and Django Concepts
"""

# GET /api/courses/ Request Journey
#
# 1. Browser sends HTTP GET request to http://127.0.0.1:8000/api/courses/
# 2. WSGI/ASGI server receives the request and passes it to Django
# 3. Middleware stack processes the request (security, sessions, auth, etc.)
# 4. URL Router (ROOT_URLCONF -> coursemanager/urls.py -> courses/urls.py) matches /api/courses/
# 5. The matched URL pattern dispatches to the course_list view function
# 6. View function queries the Course Model via Django ORM (e.g., Course.objects.all())
# 7. Database returns course records to the Model layer
# 8. View serializes data into an HttpResponse (JSON or rendered template)
# 9. Middleware processes the response on the way out
# 10. WSGI/ASGI server sends HTTP response back to the browser

# Middleware Role
#
# Middleware sits between the web server and the view. It processes every request
# before it reaches the view and every response before it leaves Django.
# Request flow: Server -> Middleware (in order) -> View -> Middleware (reverse order) -> Server
#
# Two built-in Django middleware classes:
#
# 1. django.middleware.security.SecurityMiddleware
#    Adds security enhancements such as HTTPS redirect, HSTS headers,
#    and MIME-type sniffing protection.
#
# 2. django.contrib.sessions.middleware.SessionMiddleware
#    Enables session support by reading/writing session data from cookies
#    and attaching the session to the request object.

# WSGI vs ASGI
#
# WSGI (Web Server Gateway Interface) is a synchronous standard for Python web apps.
# It handles one request at a time per worker thread. Django uses WSGI by default
# via coursemanager/wsgi.py.
#
# ASGI (Asynchronous Server Gateway Interface) supports async, WebSockets, and
# long-lived connections. Django 3.0+ supports ASGI via coursemanager/asgi.py.
#
# Switch to ASGI when you need:
# - WebSocket support (real-time features)
# - Async views and concurrent long-running requests
# - Integration with async middleware or channels

# MVC vs Django MVT
#
# MVC (Model-View-Controller):
#   Model      - Data and business logic
#   View       - Presentation layer (UI)
#   Controller - Handles user input, coordinates Model and View
#
# Django MVT (Model-View-Template):
#   Model    - Data layer (models.py) - maps directly to MVC Model
#   View     - Request handler (views.py) - does what MVC Controller does
#   Template - HTML presentation (templates/) - equivalent to MVC View
#
# A Django project is the overall configuration container.
# A Django app is a self-contained module with its own models, views, and URLs.
# One project can host many apps.

# Django Project File Roles
#
# settings.py - Central configuration: installed apps, database, middleware, templates
# urls.py     - Root URL routing; maps URL paths to views across the project
# wsgi.py     - WSGI entry point for production deployment with sync servers
# asgi.py     - ASGI entry point for async deployment and WebSocket support
