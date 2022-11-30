
#basic report included with helloanalytics
dimensions_basic_report = [
    {'name': 'ga:dateHourMinute'},
    {'name': 'ga:sourceMedium'},
    {'name': 'ga:deviceCategory'},
    {'name': 'ga:city'},
    {'name': 'ga:country'},
    {'name': 'ga:landingPagePath'},
    {'name': 'ga:pagePath'}
    ]
metrics_basic_report = [
    {'expression': 'ga:users'},     
    {'expression': 'ga:newUsers'},  
    {'expression': 'ga:pageviews'},
    {'expression': 'ga:bounces'},
    {'expression': 'ga:sessions'},
    {'expression': 'ga:goal1Completions'},
    {'expression': 'ga:timeOnPage'}
    ]

#Audience Report
dimensions_users_demographics = [
    {'name': 'ga:userGender'},
    {'name': 'ga:userAgeBracket'}
    ]
dimensions_users_geographics = [
    {'name': 'ga:language'},
    {'name': 'ga:continent'},
    {'name': 'ga:country'},
    {'name': 'ga:region'},
    {'name': 'ga:city'}
    ]
dimensions_users_overview = [
    {'name': 'ga:date'}
    ]
metrics_users_overview= [
    {'expression': 'ga:users'},     
    {'expression': 'ga:newUsers'},
    {'expression': 'ga:sessions'},
    {'expression': 'ga:sessionDuration'}, #in seconds
    {'expression': 'ga:pageviewsPerSession'},
    {'expression': 'ga:bounceRate'}
    ]

#Acquisition 
dimensions_users_acquisition = [
    {'name': 'ga:source'},
    {'name': 'ga:dataSource'}
    ]

#Ecommerce
dimensions_users_ecommerce = [
]
metrics_users_ecommerce = [
    {'expression': 'ga:transactions'}
]

#Page tracking
dimensions_users_acquisition = [
    {'name': 'ga:dateHourMinute'},
    {'name': 'ga:pagePath'},
    {'name': 'ga:secondPagePath'}
]
metrics_users_page = [
    {'expression': 'ga:users'}
]

#Google Ads
dimensions_google_ads = [
    {'name': 'ga:adPlacementDomain'}
]
metrics_google_ads = [
    {'expression': 'ga:impressions'}
]

#Just for testing
nonea = [{'expression': 'ga:users'}]

start_date = '80daysAgo'
end_date = '1daysAgo'