from app import create_app , socketio

app = create_app(port=5000,debug=True)

if __name__ == "__main__":
   socketio.run(app)

