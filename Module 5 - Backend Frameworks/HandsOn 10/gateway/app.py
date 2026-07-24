import requests
from flask import Flask, Response, request

app = Flask(__name__)

COURSE_SERVICE = 'http://127.0.0.1:5001'
STUDENT_SERVICE = 'http://127.0.0.1:5002'


def proxy_request(base_url: str, subpath: str):
    url = f'{base_url}{subpath}'
    response = requests.request(
        method=request.method,
        url=url,
        headers={k: v for k, v in request.headers if k.lower() != 'host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
        timeout=10,
    )
    excluded = {'content-encoding', 'content-length', 'transfer-encoding', 'connection'}
    headers = [(k, v) for k, v in response.raw.headers.items() if k.lower() not in excluded]
    return Response(response.content, response.status_code, headers)


@app.route('/api/courses/', defaults={'subpath': ''}, methods=['GET', 'POST'])
@app.route('/api/courses/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy_courses(subpath):
    path = f'/api/courses/{subpath}' if subpath else '/api/courses/'
    if request.query_string:
        path = f'{path}?{request.query_string.decode()}'
    return proxy_request(COURSE_SERVICE, path)


@app.route('/api/students/', defaults={'subpath': ''}, methods=['GET', 'POST'])
@app.route('/api/students/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy_students(subpath):
    path = f'/api/students/{subpath}' if subpath else '/api/students/'
    if request.query_string:
        path = f'{path}?{request.query_string.decode()}'
    return proxy_request(STUDENT_SERVICE, path)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
