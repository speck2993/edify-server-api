import app

app = app.get_app()

if __name__ == '__main__':
    print("Running app.py")
    app.run(debug=True)