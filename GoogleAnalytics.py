"""Hello Analytics Reporting API V4."""
import pandas as pd
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

class Google:
  def __init__(self,dimensions,metrics,start_date,end_date):
    self.metrics =    metrics
    self.dimensions = dimensions
    self.start_date = start_date
    self.end_date =   end_date

    self.SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
    self.KEY_FILE_LOCATION = './Keys/GoogleAnalyticsKey.json'
    self.VIEW_ID = '276986471'


def report(self):
    '''
    Gets data from google analytics, formats and returns it for the front end

    Args:
      This will be set up later to include options for date ranges and other things

    Returns:
      A dataframe of the requested analytics 
    '''

    analytics = initialize_analyticsreporting(self)

    rows = []
    rows = handle_report(self,analytics,'0',rows)

    return pd.DataFrame(list(rows))

def initialize_analyticsreporting(self):
  """
  Initializes an Analytics Reporting API V4 service object.

  Returns:
    An authorized Analytics Reporting API V4 service object.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      self.KEY_FILE_LOCATION, self.SCOPES)

  # Build the service object.
  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics


def get_report(self,analytics):
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
            'viewId': self.VIEW_ID,
            'dateRanges': [{'startDate': self.start_date, 'endDate': self.end_date}],
            'metrics': self.metrics,
            'dimensions': self.dimensions
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


def handle_report(self,analytics,pagetoken,rows):  
    """
    Formats a dataframe object from the data

    Args:
      analytics:
      pagetoken:
      rows:
    """

    response = get_report(self,analytics)

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
        return handle_report(self,analytics,pagetoken,rows)
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
