import pandas as pd
import api_keys
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


# lists
@app.route('/lists', methods=['GET'])
def get_lists_info():
    try:
        response = client.lists.get_all_lists()
        id = response['lists'][0]['id']
        print(response)
        return jsonify(id)
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


@app.route('/lists/<list_id>', methods=['DELETE'])
def delete_list(list_id):
    try:
        response = client.lists.delete_list(list_id)
        print(response)
        return jsonify("Successfully deleted.")
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


@app.route('/lists/<list_id>/members', methods=['POST'])
def add_member_to_list(list_id):
    try:
        request_data = request.get_json()
        member_info = {
            "email_address": request_data['email_address'],
            "status": request_data['status']
        }
        response = client.lists.add_list_member(list_id, member_info)
        print("response: {}".format(response))
        return jsonify(response)
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))
        return jsonify(error.text)


# Campaigns
@app.route('/campaigns', methods=['GET'])
def list_campaigns():
    try:
        response = client.campaigns.list()
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