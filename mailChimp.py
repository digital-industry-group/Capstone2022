#import Capstone2022.app.api_keys as api_keys
import api_keys as api_keys
from flask import Flask, request, jsonify
from mailchimp_marketing.api_client import ApiClientError
import mailchimp_marketing as MailchimpMarketing

app = Flask(__name__)

SERVER_PREFIX = 'us17'


client = MailchimpMarketing.Client()
client.set_config({
    "api_key": api_keys.MAIL_CHIMP_KEY,
    "server": SERVER_PREFIX
})

@app.route('/', methods=['GET'])
def index():
    return 'DIG Marketing Reports'

# Campaigns
@app.route('/campaigns', methods=['GET'])
def list_campaigns():
    try:
        response = client.campaigns.list()
        camp = response['campaigns']
        print(response)
        return jsonify(camp)
    except ApiClientError as error:
        print("Error: {}".format(error.text))
        return jsonify(error.text)

# Reports
@app.route('/reports', methods=['GET'])
def reports():
    try:
        response = client.reports.get_all_campaign_reports()
        print(response)
        return jsonify(response)
    except ApiClientError as error:
        print("Error: {}".format(error.text))
        return jsonify(error.text)

#Click Reports      

@app.route('/reports/<campaign_id>/clicks', methods = ['GET']) 
def clicks(campaign_id):
    try:     
        response = client.reports.get_campaign_click_details(campaign_id)
        print(response)
        return jsonify(response)
    except ApiClientError as error:
        print("Error: {}".format(error.text))
        return jsonify(error.text)

 
# lists
@app.route('/lists', methods=['GET'])
def get_lists_info():
    try:
        response = client.lists.get_all_lists()
        id = response['lists'][0]['id']
        print(response)
        return jsonify(response)
    except ApiClientError as error:
        print("Error: {}".format(error.text))
        return jsonify(error.text)
    except IndexError:
        print("Error: IndexError, lists: {}")
        return jsonify("Error: IndexError, lists: {}")


@app.route('/lists', methods=['POST'])
def add_list():
    try:
        request_data = request.get_json()
        lists_info = {
            "name": request_data['name'],
            "permission_reminder": "permission_reminder",
            "email_type_option": True,
            "contact": {
                "company": "company",
                "address1": "address1",
                "city": "city",
                "country": "country",
                "state": "state",
                "zip": "zip"
            },
            "campaign_defaults": {
                "from_name": "from_name",
                "from_email": "n574838382000@gmail.com",
                "subject": "subject",
                "language": "language"
            }
        }
        response = client.lists.create_list(lists_info)
        print(response)
        return jsonify(response)
    except ApiClientError as error:
        print("Error: {}".format(error.text))
        return jsonify(error.text)


# members
@app.route('/lists/<list_id>/members', methods=['GET'])
def list_members_info(list_id):
    try:
        response = client.lists.get_list_members_info(list_id)
        print(response)
        return jsonify(response)
    except ApiClientError as error:
        print("Error: {}".format(error.text))
        return jsonify(error.text)




@app.route('/campaigns', methods=['POST'])
def add_campaign():
    try:
        response = client.campaigns.create({"type": "regular"})
        print(response)
        return jsonify(response)
    except ApiClientError as error:
        print("Error: {}".format(error.text))
        return jsonify(error.text)


@app.route('/campaigns/<campaign_id>/actions/send', methods=['POST'])
def send_campaign(campaign_id):
    try:
        response = client.campaigns.send(campaign_id)
        print(response)
        return jsonify(response)
    except ApiClientError as error:
        print("Error: {}".format(error.text))
        return jsonify(error.text)


@app.route('/campaigns/<campaign_id>/actions/test', methods=['POST'])
def send_test_email(campaign_id):
    try:
        response = client.campaigns.send_test_email(campaign_id, {"test_emails": [
                                                    "n574838382000@gmail.com"], "send_type": "plaintext"})
        print(response)
        return jsonify(True)
    except ApiClientError as error:
        print("Error: {}".format(error.text))
        return jsonify(error.text)


# ping
@app.route('/ping', methods=['GET'])
def ping():
    try:
        response = client.ping.get()
        print(response)
        return jsonify(response)
    except ApiClientError as error:
        print("Error: {}".format(error.text))
        return jsonify(error.text)
 

if __name__ == '__main__':
    app.run(debug=True)