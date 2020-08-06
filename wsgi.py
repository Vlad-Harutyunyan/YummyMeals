from app import create_app , socketio

app = create_app(port=5008,debug=True)

if __name__ == "__main__":
   socketio.run(app)

