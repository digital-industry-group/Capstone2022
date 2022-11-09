import pandas as pd
import GoogleAnalytics as ga
from app import app
import json

dimensions_list = [
    {'name': 'ga:dateHourMinute'},
    {'name': 'ga:sourceMedium'},
    {'name': 'ga:deviceCategory'},
    {'name': 'ga:city'},
    {'name': 'ga:country'},
    {'name': 'ga:landingPagePath'},
    {'name': 'ga:pagePath'}
    ]

metrics_list = [
    {'expression': 'ga:users'},     
    {'expression': 'ga:newUsers'},  
    {'expression': 'ga:pageviews'},
    {'expression': 'ga:bounces'},
    {'expression': 'ga:sessions'},
    {'expression': 'ga:goal1Completions'},
    {'expression': 'ga:timeOnPage'}
    ]
start_date = '5daysAgo'
end_date = '1daysAgo'

'''dimensions_list = [
    {'name': 'ga:source'},
    {'name': 'ga:medium'},
    {'name': 'ga:referralPath'},
    {'name': 'ga:keyword'}
    ]

metrics_list = [
    {'expression': 'ga:users'}
    ]
'''

class Report_Controller():
    def __init__(self,ga_dimensions,ga_metrics,s_date,e_date):
        self.ga_dimensions = ga_dimensions
        self.ga_metrics = ga_metrics
        self.s_date = s_date
        self.e_date = e_date

    def run_ga_report(self):
        ga_report = ga.Google_Data(self.ga_dimensions,self.ga_metrics,self.s_date,self.e_date)
        df = ga_report.report()
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        self.df_json_conv(df)

    def df_json_conv(self,df):
        df_json = df.to_json(orient = 'records')
        print(df_json)
        return df_json

    def set_report_type(self,input):
        #later
        return

r = Report_Controller(dimensions_list,metrics_list,start_date,end_date)
r.run_ga_report()
