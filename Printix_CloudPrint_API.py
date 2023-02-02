import requests
import json
from requests.structures import CaseInsensitiveDict


client_id= '' #Please refer to https://printix.github.io/ on how to retrieve the id and secret
client_secret= ''

def auth():
    url = 'https://auth.printix.net/oauth/token'
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    data = 'grant_type=client_credentials&client_id='+str(client_id)+'&client_secret='+str(client_secret)
    resp = requests.post(url, headers=headers, data=data)
    loads = json.loads(resp.content)
    return loads['access_token']

def refresh_auth(refresh_token):
    url = 'https://auth.printix.net/oauth/token'
    headers = CaseInsensitiveDict() 
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    data = 'grant_type=refresh_token&client_id='+str(client_id)+'&refresh_token='+str(refresh_token)
    resp = requests.post(url, headers=headers, data=data)
    return 

def get_root():
    access_token = auth()
    url = 'https://api.printix.net/cloudprint'
    headers = {
                'Accept': 'application/json',
                'Authorization' : 'Bearer'+access_token+''}
    resp = requests.get(url, headers=headers)
    loads = json.loads(resp.content)
    href = loads['_links']['cosy-nfr.printix.net']['href']
    result = href.split('{')
    return result[0]


def get_printer_list():
    access_token = auth()
    url = get_root()
    headers = {
                'Accept': 'application/json',
                'Authorization' : 'Bearer'+access_token+''}
    resp = requests.get(url, headers=headers)
    loads = json.loads(resp.content)
    printer_list = loads['printers']
    filtered = [x for x in printer_list if x['connectionStatus'] == 'ONLINE']
    return filtered

#return specific printer detail

def get_printer():
    access_token = auth()
    url = get_root()
    headers = {
                'Accept': 'application/json',
                'Authorization' : 'Bearer'+access_token+''}
    resp = requests.get(url, headers=headers)
    loads = json.loads(resp.content)
    printer_list = loads['printers']
    filtered = [x for x in printer_list if x['connectionStatus'] == 'ONLINE']
    return filtered[1]['_links']['self']['href']


def get_job_list():
    access_token = auth()
    url = (get_root().split('printers'))
    job_url = url[0]+'jobs'+url[1]
    headers = {
                'Accept': 'application/json',
                'Authorization' : 'Bearer'+access_token+''}
    resp = requests.get(job_url, headers=headers)
    loads = json.loads(resp.content)
    return loads

def submit_job(title):
    access_token = auth()
    printer_url = get_printer()
    url = printer_url+'/submit'
    params = {'title' : title}
    headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'version' : '1.1',
                'Authorization' : 'Bearer'+access_token,
                'Content-Length': '137'}
    data = {
            "color" : "false",
            "duplex" : "NONE",
            "page_orientation" : "AUTO",
            "copies" : 1,
            "media_size" : "A4",
            "scaling" : "NOSCALE"
            }
    resp = requests.post(url, headers=headers, params=params ,json=data)
    loads = json.loads(resp.content)
    return loads


 
def upload_job(**params):
    url =params["cloud_storage_urls"]
    Authorization = 'Bearer' + params["token"]
    headers = {
            'Content-Type': 'application/pdf',
            'Authorization': Authorization
            }
    files ={'file': open(params["path"], 'rb')}
    resp = requests.put(url,headers=headers,files=files)
    return resp

def completeUpload(url):
    access_token = auth()
    headers = {
            'Accept': 'application/json',
            'Authorization' : 'Bearer'+access_token
    }
    resp = requests.post(url,headers=headers)
    loads = json.loads(resp.content)
    return loads

def retrieve_job(url):
    access_token = auth()
    headers = {
            'Accept': 'application/json',
            'Authorization' : 'Bearer'+ access_token
            }
    resp = requests.get(url,headers=headers)
    loads = json.loads(resp.content)
    return loads

def delete_job(url):
    urls = url+'/delete'
    print(urls)
    access_token = auth()
    headers = {
            'Accept': 'application/json',
            'Authorization' : 'Bearer'+ access_token
            }
    resp = requests.post(urls,headers=headers)
    loads = json.loads(resp.content)
    
    return loads

