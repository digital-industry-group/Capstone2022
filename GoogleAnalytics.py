"""Hello Analytics Reporting API V4."""
import pandas as pd
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = './KeyFile.json'
VIEW_ID = '276986471'


def initialize_analyticsreporting():
  """
  Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)

  # Build the service object.
  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics


def get_report(analytics):
  """
  Queries the Analytics Reporting API V4.

  Args:
    analytics: An authorized Analytics Reporting API V4 service object.
  Returns:
    The Analytics Reporting API V4 response.
  """
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
            'viewId': VIEW_ID,
            'dateRanges': [{'startDate': '3daysAgo', 'endDate': 'today'}],
            'metrics': [
                {'expression': 'ga:users'},
                {'expression': 'ga:newUsers'},
                {'expression': 'ga:pageviews'},
                {'expression': 'ga:bounces'},
                {'expression': 'ga:sessions'},
                {'expression': 'ga:goal1Completions'},
                {'expression': 'ga:timeOnPage'}
            ],
            'dimensions': [
                {'name': 'ga:date'},
                {'name': 'ga:dateHour'},
                {'name': 'ga:dateHourMinute'},
                {'name': 'ga:sourceMedium'},
                {'name': 'ga:deviceCategory'},
                {'name': 'ga:city'},
                {'name': 'ga:country'},
                {'name': 'ga:landingPagePath'},
                {'name': 'ga:pagePath'}
            ]
        }]
      }
  ).execute()


def print_response(response):
  """
  Parses and prints the Analytics Reporting API V4 response.

  Args:
    response: An Analytics Reporting API V4 response.
  """
  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

    for row in report.get('data', {}).get('rows', []):
        dimensions = row.get('dimensions', [])
        dateRangeValues = row.get('metrics', [])

        for header, dimension in zip(dimensionHeaders, dimensions):
            print(header + ': ', dimension)

        for i, values in enumerate(dateRangeValues):
            print('Date range:', str(i))
            for metricHeader, value in zip(metricHeaders, values.get('values')):
                print(metricHeader.get('name') + ':', value)


def handle_report(analytics,pagetoken,rows):  
    """
    Formats a dataframe object from the data

    Args:
      analytics:
      pagetoken:
      rows:
    """

    response = get_report(analytics)

    #Header, Dimentions Headers, Metric Headers 
    columnHeader = response.get("reports")[0].get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
    

    #Pagination
    pagetoken = response.get("reports")[0].get('nextPageToken', None)
    
    #Rows
    rowsNew = response.get("reports")[0].get('data', {}).get('rows', [])
    rows = rows + rowsNew
    #print("len(rows): " + str(len(rows)))

    #Recursivly query next page
    if pagetoken != None:
        return handle_report(analytics,pagetoken,rows)
    else:
        #nicer results
        nicerows=[]
        for row in rows:
            dic={}
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            for header, dimension in zip(dimensionHeaders, dimensions):
                dic[header] = dimension

            for i, values in enumerate(dateRangeValues):
                for metric, value in zip(metricHeaders, values.get('values')):
                    if ',' in value or ',' in value:
                        dic[metric.get('name')] = float(value)
                    else:
                        dic[metric.get('name')] = float(value)
            nicerows.append(dic)
        return nicerows

def googleAnalytics():
    '''
    Gets data from google analytics, formats and returns it for the front end

    Args:
      This will be set up later to include options for date ranges and other things

    Returns:
      A dataframe of the requested analytics 
    '''

    analytics = initialize_analyticsreporting()

    dfanalytics = []

    rows = []
    rows = handle_report(analytics,'0',rows)

    #dfanalytics = 
    return pd.DataFrame(list(rows))
    '''
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    f = open("Hello.txt", "w")
    print(dfanalytics, file=f)
    dfanalytics.to_csv("HelloCSV.csv", sep='\t')
    '''
    #return dfanalytics
