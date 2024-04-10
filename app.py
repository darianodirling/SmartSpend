
from website import create_app, create_database

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

app = create_app()

with app.app_context():
    create_database(app)

if __name__ == "__main__":
    app.run(debug=True)
