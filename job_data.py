import requests

#Accepts an array of keywords, and returns a dictionary with results for each keyword.
def query_keywords(api_url, app_id, api_key, keywords):
    results = {}
    for keyword in keywords:
        url = f"{api_url}?app_id={app_id}&app_key={api_key}&what={keyword}&content-type=application/json"
        try:
            response = requests.get(url)
            # Check if the request was successful
            if response.status_code == 200:
                results[keyword] = response.json()
            else:
                results[keyword] = f"Error: Received status code {response.status_code}"
        except requests.RequestException as e:
            results[keyword] = f"Request failed: {e}"
    return results

# API key and app ID
api_url = 'http://api.adzuna.com/v1/api/jobs/us/search/1'
app_id = ' '
api_key = ''
keywords = ['Software Developer', 'Data Scientist', 'Product Manager']

job_data = query_keywords(api_url, app_id, api_key, keywords)
for keyword, data in job_data.items():
    print(f"Results for {keyword}: {data}")
