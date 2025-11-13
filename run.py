# run.py  http://localhost:8001
from app import create_app

app = create_app()

@app.after_request
def add_csp_header(response):
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' https://code.jquery.com https://cdn.jsdelivr.net; "
        "style-src 'self'; "  
        "img-src 'self' data:; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "frame-src 'none'; "
        "object-src 'none'; "
        "media-src 'self'; "
        "child-src 'none'; "
        "form-action 'self'; "
        "base-uri 'self';"
    )
    response.headers['X-Frame-Options'] = 'DENY'

    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8001, debug=False)