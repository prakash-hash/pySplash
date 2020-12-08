#! /usr/bin/env python3
def url(api_key):
	url = "https://api.unsplash.com/search/photos/?client_id={}".format(api_key['Access Key'])
	return url
