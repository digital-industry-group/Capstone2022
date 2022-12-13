from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from mailchimp_marketing.api_client import ApiClientError
import mailchimp_marketing as MailchimpMarketing
import os
from schemas import ListSchema

blp = Blueprint("MailChimp", "mailchimp", description="Operations on mailchimp")

client = MailchimpMarketing.Client()
client.set_config({
    "api_key": os.environ.get("MAILCHIMP_API_KEY"),
    "server": os.environ.get("MAILCHIMP_SERVER_PREFIX")
})


@blp.route("/reports")
class Reports(MethodView):
    @blp.response(200)
    def get(self):
        # item = ItemModel.find_by_name(name)
        # if item:
        #     return item
        # abort(404, message="Item not found")
        try:
            response = client.reports.get_all_campaign_reports()
            # get_data = jsonify(response)
            reports = response['reports']
            # print('reports', reports)
            total_items = response['total_items']
            # print('total items', total_items)
            final_report = [{
                'id': reports[x]['id'],
                'campaign_title': reports[x]['campaign_title'],
                'list_id': reports[x]['list_id'],
                'list_name': reports[x]['list_name'],
                "subject_line": reports[x]['subject_line'],
                "emails_sent": reports[x]['emails_sent'],
                "unsubscribed": reports[x]['unsubscribed'],
                "send_time": reports[x]['send_time'],
                # "rss_last_send": reports[x]['rss_last_send'],
                "bounces": reports[x]['bounces'],
                "forwards": reports[x]['forwards'],
                "opens": reports[x]['opens'],
                "clicks": reports[x]['clicks'],
                "list_stats": reports[x]['list_stats']
                #"timeseries": reports[x]['timeseries']
            } for x in range(total_items)]

            output = {'reports': final_report, 'total_items': total_items}
            return jsonify(output)
        except ApiClientError as error:
            print("Error: {}".format(error.text))
            return jsonify(error.text)


@blp.route("/campaigns")
class Campaigns(MethodView):
    @blp.response(200)
    def get(self):
        """List of Campaigns"""
        try:
            response = client.campaigns.list()
            camp = response['campaigns']
            print(response)
            return jsonify(camp)
        except ApiClientError as error:
            print("Error: {}".format(error.text))
            return jsonify(error.text)


@blp.route("/reports/<campaign_id>/clicks")
class Clicks(MethodView):
    @blp.response(200)
    def get(self, campaign_id):
        try:
            response = client.reports.get_campaign_click_details(campaign_id)
            # print(response)
            return jsonify(response)
        except ApiClientError as error:
            print("Error: {}".format(error.text))
            return jsonify(error.text)


@blp.route("/lists")
class Lists(MethodView):
    @blp.response(200)
    def get(self):
        """Get Lists Info"""
        try:
            response = client.lists.get_all_lists()
            id = response['lists'][0]['id']
            # print(response)
            return jsonify(response)
        except ApiClientError as error:
            print("Error: {}".format(error.text))
            return jsonify(error.text)
        except IndexError:
            print("Error: IndexError, lists: {}")
            return jsonify("Error: IndexError, lists: {}")

    @blp.arguments(ListSchema)
    @blp.response(201)
    def post(self, list_data):
        """Add list"""
        try:
            print(list_data['name'])
            lists_info = {
                "name": list_data['name'],
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
            # print(response)
            return jsonify(response)
        except ApiClientError as error:
            print("Error: {}".format(error.text))
            return jsonify(error.text)


@blp.route("/lists/<list_id>/members")
class ListsMemberInfo(MethodView):
    @blp.response(200)
    def get(self, list_id):
        """Get Lists member info by list_id"""
        try:
            response = client.lists.get_list_members_info(list_id)
            # print(response)
            return jsonify(response)
        except ApiClientError as error:
            print("Error: {}".format(error.text))
            return jsonify(error.text)


@blp.route("/ping")
class Ping(MethodView):
    @blp.response(200)
    def get(self):
        """Get Ping"""
        try:
            response = client.ping.get()
            # print(response)
            return jsonify(response)
        except ApiClientError as error:
            print("Error: {}".format(error.text))
            return jsonify(error.text)
