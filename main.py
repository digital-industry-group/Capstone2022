import pandas as pd
import GoogleAnalytics as ga
#from app import app

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
start_date = '9daysAgo'
end_date = 'today'

report = ga.Google(dimensions_list,metrics_list,start_date,end_date)
df = ga.report(report)


#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)
#df.to_csv("GoogleAnalytics.csv", sep='\t')


#df.to_json('temp.json', orient='records', lines=True)