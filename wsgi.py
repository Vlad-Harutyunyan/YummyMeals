from app import create_app

app = create_app()


#commands  flask db init , flask db migrate , flask db upgrade

if __name__ == "__main__":
   app.run(port=5000,debug=True)
