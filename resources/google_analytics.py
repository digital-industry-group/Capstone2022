from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import pandas as pd
from repository import GoogleAnalytics as ga
from repository import dimensionsMetricsGA as dm
import json
import copy

#Blueprints provide separation at the Flask level dividing flask app into multiple sections
blp = Blueprint("GoogleAnalytics", "googleanalytics", description="Operations on Google analytics")

def remove_GA(input):
    output = copy.deepcopy(input)
    for x in range(len(input)):
        print(x,"\n")
        for old_key in input[x]:
            print(old_key)
            new_key = old_key.replace("ga:","")
            output[x][new_key] = output[x].pop(old_key)
    return output    

class Report_Controller():
    def __init__(self, ga_dimensions, ga_metrics, s_date, e_date):
        self.ga_dimensions = ga_dimensions
        self.ga_metrics = ga_metrics
        if type(s_date) == int:
            self.s_date = str(s_date) + 'daysAgo'
            self.e_date = str(e_date) + 'daysAgo'
        elif type(s_date) == str:
            self.s_date = s_date
            self.e_date = e_date

    def run_ga_report_csv(self, temp):
        ga_report = ga.Google_Data(self.ga_dimensions, self.ga_metrics, self.s_date, self.e_date)
        df = ga_report.report()
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        df.to_csv(temp, sep=',')
        self.df_json_conv(df)

    def run_ga_report(self):
        ga_report = ga.Google_Data(self.ga_dimensions, self.ga_metrics, self.s_date, self.e_date)
        df = ga_report.report()
        # pd.set_option('display.max_columns', None)
        # pd.set_option('display.max_rows', None)
        # self.df_json_conv(df)
        return self.df_json_conv(df)

    def df_json_conv(self, df):
        df_json = df.to_json(orient='records')
        return df_json

    def set_report_type(self, input):
        # later
        return


@blp.route("/basic")
class BasicReportData(MethodView):
    @blp.response(200)
    def get(self):
        basic_report = Report_Controller(dm.dimensions_basic_report, dm.metrics_basic_report, dm.start_date,
                                         dm.end_date)
        output = json.loads(basic_report.run_ga_report())
        #print(type(output))
        out = remove_GA(output)
        return jsonify(out)


@blp.route("/user/overview")
class UsersOverviewData(MethodView):
    @blp.response(200)
    def get(self):
        users_overview = Report_Controller(dm.dimensions_users_overview, dm.metrics_users_overview, 2, 0)
        output = json.loads(users_overview.run_ga_report())

        out = remove_GA(output)
        return jsonify(out)


@blp.route("/user/geographics")
class UsersGeographicsData(MethodView):
    @blp.response(200)
    def get(self):
        users_geographics = Report_Controller(dm.dimensions_users_geographics, dm.metrics_users_overview, dm.start_date,
                                              dm.end_date)
        output = json.loads(users_geographics.run_ga_report())
        out = remove_GA(output)
        return jsonify(out)


@blp.route("/user/acquisition")
class UsersAcquisitionData(MethodView):
    @blp.response(200)
    def get(self):
        users_acquisition = Report_Controller(dm.dimensions_users_acquisition, dm.metrics_users_overview, 80, 1)
        output = json.loads(users_acquisition.run_ga_report())
        out = remove_GA(output)
        return jsonify(out)