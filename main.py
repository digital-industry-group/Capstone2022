import pandas as pd
import GoogleAnalytics as ga
from app import app
import json
#import mailChimp as mc
import dimensionsMetricsGA as dm
from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class Report_Controller():
    def __init__(self,ga_dimensions,ga_metrics,s_date,e_date):
        self.ga_dimensions = ga_dimensions
        self.ga_metrics = ga_metrics
        if type(s_date) == int:
            self.s_date = str(s_date) + 'daysAgo'
            self.e_date = str(e_date) + 'daysAgo'
        elif type(s_date) == str:
            self.s_date = s_date
            self.e_date = e_date

    def run_ga_report_csv(self,temp):
        ga_report = ga.Google_Data(self.ga_dimensions,self.ga_metrics,self.s_date,self.e_date)
        df = ga_report.report()
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        df.to_csv(temp, sep=',')
        self.df_json_conv(df)

    def run_ga_report(self):
        ga_report = ga.Google_Data(self.ga_dimensions,self.ga_metrics,self.s_date,self.e_date)
        df = ga_report.report()
        #pd.set_option('display.max_columns', None)
        #pd.set_option('display.max_rows', None)
        #self.df_json_conv(df)
        return self.df_json_conv(df)


    def df_json_conv(self,df):
        df_json = df.to_json(orient = 'records')
        return df_json

    def set_report_type(self,input):
        #later
        return



class basic_report_data(Resource):
    def get(self):
        basic_report = Report_Controller(dm.dimensions_basic_report,dm.metrics_basic_report,dm.start_date,dm.end_date)
        return basic_report.run_ga_report()
api.add_resource(basic_report_data, "/basic")

class users_overview_data(Resource):
    def get(self):
        users_overview = Report_Controller(dm.dimensions_users_overview,dm.metrics_users_overview,2,0)
        return users_overview.run_ga_report()
api.add_resource(users_overview_data, "/user/overview")

class users_geographics_data(Resource):
    def get(self):
        users_geographics = Report_Controller(dm.dimensions_users_geographics,dm.metrics_users_overview,dm.start_date,dm.end_date)
        return users_geographics.run_ga_report()
api.add_resource(users_geographics_data, "/user/geographics")

class users_acquisition_data(Resource):
    def get(self):
        users_acquisition = Report_Controller(dm.dimensions_users_acquisition,dm.metrics_users_overview,80,1)
        return users_acquisition.run_ga_report()
api.add_resource(users_acquisition_data, "/user/acquisition")


#Current website isn't tracking demographics
users_demographics = Report_Controller(dm.dimensions_users_demographics,dm.metrics_users_overview,dm.start_date,dm.end_date)
users_demographics.run_ga_report_csv("Reports/users_demographics.csv")

#current website isn't tracking ecommerce
users_ecommerce = Report_Controller(dm.dimensions_users_overview,dm.metrics_users_ecommerce,dm.start_date,dm.end_date)
users_ecommerce.run_ga_report_csv("Reports/users_ecommerce.csv")

#currently having issue with creating a report of the path
users_page = Report_Controller(dm.dimensions_users_acquisition,dm.metrics_users_page,dm.start_date,dm.end_date)
users_page.run_ga_report_csv("Reports/users_page.csv")

#as far as I can tell, current website isn't using google ads
google_ads = Report_Controller(dm.dimensions_google_ads,dm.metrics_google_ads,dm.start_date,dm.end_date)
google_ads.run_ga_report_csv("Reports/google_ads.csv")


if __name__=="__main__":
    app.run(debug=True)