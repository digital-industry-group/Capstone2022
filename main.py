import pandas as pd
import GoogleAnalytics as ga
#from app import app


df = ga.googleAnalytics()
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
df.to_csv("GoogleAnalyticsCSV.csv", sep='\t')