from app import app

if __name__ == "__main__":
    # DEVELOPMENT
    app.run(debug=True, port=5001)
else:
    # PRODUCTION
    gunicorn_app = app
