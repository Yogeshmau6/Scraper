#!/usr/bin/env python
# coding: utf-8

# Required Python Modules

# pip install requests
# pip install BeautifulSoup4
# pip install mechanicalsoup
# pip install Pillow

import requests
from bs4 import BeautifulSoup
from PIL import Image
from skimage import io
import mechanicalsoup
from io import BytesIO

dri_lic_no = input("Enter Driving Liscense Number : ")
dob = input("Enter Date of Birth in dd-mm-yyyy Format : ")
# DL-0420110149646
# 09-02-1976

def start_p() :
    browser = mechanicalsoup.StatefulBrowser()
    browser.open("https://parivahan.gov.in/rcdlstatus/?pur_cd=101")
    mg1= str(browser.get_current_page().find_all('img')[1])
    img2 = mg1.split('"/')[1]
    img3 = img2.replace("amp;", '')
    img4 = "https://parivahan.gov.in/" + img3
    return img4,browser
img4,browser = start_p()

def get_captcha(img4) :
    response = requests.get(img4)
    img = Image.open(BytesIO(response.content))
    img.show()
    cap_is = input("enter captcha : ")
    return cap_is
cap_is= get_captcha(img4)

browser.select_form('form')
browser['form_rcdl:tf_dlNO'] =dri_lic_no
browser['form_rcdl:tf_dob_input'] = dob
browser['form_rcdl:j_idt32:CaptchaID'] = cap_is
response = browser.submit_selected()

def parse_res(response):
    if ("Verification code does not match." not in response.text):
        print("Success Login")
        return response
    else:
        print("Login failed")
        img4,browser = start_p()
        cap_is = get_captcha(img4)
        browser.select_form('form')
        browser['form_rcdl:tf_dlNO'] =dri_lic_no
        browser['form_rcdl:tf_dob_input'] = dob
        browser['form_rcdl:j_idt32:CaptchaID'] = cap_is
        response = browser.submit_selected()
        return parse_res(response)
response = parse_res(response)

print(type(response))
print(response)
type(response.text)
res1 = response.text

output1 = open("htmlfile1.html", "w")
output1.write(res1)
output1.close()

with open("htmlfile1.html", "r") as f:
    contents = f.read()
    soup = BeautifulSoup(contents, 'lxml')

list1 = {}
for j in soup.find(class_="table table-responsive table-striped table-condensed table-bordered").find_all("tr") :
    lis =[]
    for k in j.find_all("td") :
        lis.append(k.text)
    list1[lis[0]] = lis[1]
# list1


list2 ={}
i = soup.find(class_="table table-responsive table-striped table-condensed table-bordered data-table")
for j in i.find_all("tr") :
    lis ={}
    lis[j.find_all("td")[0].text] =[{j.find_all("td")[1].text},{j.find_all("td")[2].text}]
    list2.update(lis)
# list2


list3 ={}
l1 =[]
l2 =[]
s1=[]
s2=[]
s3=[]
a,b,c=0,1,2

i = soup.find(class_="ui-datatable-tablewrapper")
for j in i.find_all("th") :
    l1.append(j.text)
q = i.find(class_="ui-datatable-data ui-widget-content")
for r in q.find_all(class_="ui-widget-content ui-datatable-even"):
    for p in r.find_all("td") :
        l2.append(p.text)

for l in range(len(l2)//3) :
    s1.append(l2[a])
    s2.append(l2[b])
    s3.append(l2[c])
    a += 3
    b += 3
    c += 3

list3[l1[0]] = [s1][0]
list3[l1[1]] = [s2][0]
list3[l1[2]] = [s3][0]

# list3

list1.update(list2)
list1.update(list3)
print(list1)



