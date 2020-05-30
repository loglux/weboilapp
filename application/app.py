from application import create_app
from flask_bootstrap import Bootstrap

app = create_app()
bpptstrap = Bootstrap(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0')