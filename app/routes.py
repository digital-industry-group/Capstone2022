#from app import app
from flask import jsonify
from api_keys import MAIL_CHIMP_KEY
import requests




@app.route('/test')
def test():
    data = {
        "response": "hello",
        "other stuff": "there"
    }

    return jsonify(data)

    
@app.route("/mailChimp")
def show_book_info():
    """Return test data for MailChimp."""

    # test_id = cf88bd0ae9
  

    resp = requests.get('https://my.website.com/rest/path', auth= ('anystring', MAIL_CHIMP_KEY))

        

    mail_chimp = resp.json()

    # using the APIs JSON data, return that to browser
    return jsonify(book_data)