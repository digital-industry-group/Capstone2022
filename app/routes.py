from app import app
from flask import jsonify

@app.route('/test')
def test():
    data = {
        "response": "hello",
        "other stuff": "there"
    }

    return jsonify(data)
