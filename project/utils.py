import requests


url = "https://supersent.in/api/send-email/"

def send_mail(to,subject,content):
    data = {
        "subject":subject,
        "to_email":to,
        "context":{
            "message":content
        },
        "api_key":"25a36e7d3c7f4e3" # change this if needed
    }
    res = requests.post(url=url,headers={},json=data)
    print("Response of Sending Email : ",res.text,"\n")