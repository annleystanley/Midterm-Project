#!/usr/bin/env python
# coding: utf-8

# In[18]:


# Foursquare API


# In[11]:


def fsq_instructions():
    print('Reset the json response using "fsq_data_resto =[]" before running api_loop so the dataframe doesn\'t stack if you run the loop again')
    print('-----')
    print('Set your foursquare API key as "foursquare_secret = os.environ[\'FSQ_API\']"')
    print('-----')
    print('Function assumes location dataframe is named \'nyc_geo_df\' & that latitudes are in [2] and longitudes are in [3]')


# In[ ]:


# function for accessing desired information from the FSQ API

def fsq_locations (lat, lon, cat):
    
    """
        Returns a dataframe containing parsed json on a given location
    
    Parameters:
        lat (str): The latitude of the search area
        lon (str): The latitude of the search area
        cat (str): The poi category to return information on
    
    Returns:
        necessary framework to run the api_loop function
    """
    # construct url
    url= 'https://api.foursquare.com/v3/places/search?ll=' + lat + ',' + lon +'&radius=1000&categories=' + cat + '&limit=25&fields=name,distance,price,geocodes,rating'
    
    # create dictionary for headers
    headers = {"Accept": "application/json",
              'Authorization' : foursquare_secret}    
        
    # perform get request
    response = requests.get(url, headers=headers)

    # process request into usable JSON file
    fsq_response = json.loads(response.text)
    fsq_data_resto.append(fsq_response)
    
    # converts normalized JSON into a dataframe
    df = pd.json_normalize(fsq_data_resto,['results'])
    df['req_cat'] = cat
    
    # convert dataframe to global variable that can be accessed outside of the function
    global fsq_df
    fsq_df = df
    
    return


# In[ ]:


# Loop for iterating fsq_location function throughout geographic dataframe
def fsq_api_loop(cat):
    """
    Iterates through the nyc_geo_df, and the fsq_locations function.
    
    Parameters:
        cat (str): desired POI category
    Returns:
        fsq_df: a dataframe containing results from the api request

    """
    num_rows = nyc_geo_df.shape[0]
    row_count = 0


    while row_count < num_rows:
        fsq_locations((nyc_geo_df.iloc[row_count,2]),(nyc_geo_df.iloc[row_count,3]),cat)
        row_count +=1


# In[19]:


# Yelp API


# In[16]:


def yelp_instructions():
    print('Reset the json response using "yelp_data_resto=[]" before running api_loop so the dataframe doesn\'t stack if you run the loop again')
    print('-----')
    print('Set your yelp API key as "yelp_secret = os.environ[\'YELP_API\']"')
    print('-----')
    print('Function assumes location dataframe is named \'nyc_geo_df\' & that latitudes are in [2] and longitudes are in [3]')


# In[17]:


yelp_instructions()


# In[ ]:


# function for accessing desired information from the yelp API

def yelp_locations (lat, lon, cat):
    
    """
        Returns a dataframe containing parsed json on a given location
    
    Parameters:
        lat (str): The latitude of the search area
        lon (str): The latitude of the search area
        cat (str): The poi category to return information on
    
    Returns:
        necessary framework to run the api_loop function
    """
    # construct url
    url= 'https://api.yelp.com/v3/businesses/search?latitude=' + lat + '&longitude=' + lon +'&radius=1000&limit=25&categories=' + cat
    
    # create dictionary for headers
    headers = {"Accept": "application/json",
              'Authorization' : 'Bearer '+ yelp_secret}    
        
    # perform get request
    response = requests.get(url, headers=headers)

    # process request into usable JSON file
    yelp_response = json.loads(response.text)
    yelp_data_resto.append(yelp_response)
    
    # converts normalized JSON into a dataframe
    df = pd.json_normalize(yelp_data_resto,['businesses'])
    df['req_cat'] = cat
    
    # convert dataframe to global variable that can be accessed outside of the function
    global yelp_df
    yelp_df = df
    #print(yelp_response)
    return


# In[ ]:


def yelp_api_loop(cat):
    # Loop for iterating fsq_location function throughout geographic dataframe
    """
    Iterates through the nyc_geo_df, and the yelp_locations function.
    
    Parameters:
        cat (str): desired POI category
    Returns:
        yelp_df: a dataframe containing results from the api request

    """
    num_rows = nyc_geo_df.shape[0]
    row_count = 0


    while row_count < num_rows:
        yelp_locations((nyc_geo_df.iloc[row_count,2]),(nyc_geo_df.iloc[row_count,3]),cat)
        row_count +=1


# In[ ]:


# Google Places Api


# In[ ]:


def gp_instructions():
    print('Reset the json response using "gp_data_resto=[]" before running api_loop so the dataframe doesn\'t stack if you run the loop again')
    print('-----')
    print('Set your yelp API key as "gp_secret = os.environ[\'GP_API\']"')
    print('-----')
    print('Function assumes location dataframe is named \'nyc_geo_df\' & that latitude & longitude are combined together in [4]')


# In[ ]:


# restaurant category in google places = restaurant
# function for accessing desired information from the Google Places API

def gp_locations (lat_lon, cat):
    
    """
        Returns a dataframe containing parsed json on a given location
    
    Parameters:
        lat_lon (str): The latitude & longitude of the search area (pre-formatted to fit google's preferred formatting)
        cat (str): The poi category to return information on
    
    Returns:
        necessary framework to run the api_loop function
    """
    # construct url
    url= 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + lat_lon + '&radius=1000&type='+ cat + '&key=' + gp_secret
    
    # create dictionary for headers
    headers = {}
    #payload = {}
        
    # perform get request
    response = requests.get(url, headers=headers)

    # process request into usable JSON file
    gp_response = json.loads(response.text)
    gp_data_resto.append(gp_response)
    
    # converts normalized JSON into a dataframe
    df = pd.json_normalize(gp_data_resto,['results'])
    df['req_cat'] = cat
    
    # convert dataframe to global variable that can be accessed outside of the function
    global gp_df
    gp_df = df
    
    return


# In[ ]:


def gp_api_loop(cat):
    # Loop for iterating fsq_location function throughout geographic dataframe
    """
    Iterates through the nyc_geo_df, and the gp_locations function.
    
    Parameters:
        cat (str): desired POI category
    Returns:
        gp_df: a dataframe containing results from the api request

    """
    num_rows = nyc_geo_df.shape[0]
    row_count = 0


    while row_count < num_rows:
        gp_locations((nyc_geo_df.iloc[row_count,4]),cat)
        row_count +=1


# In[ ]:





# In[ ]:




