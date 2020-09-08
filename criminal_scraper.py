import requests
from bs4 import BeautifulSoup 
import json



def find_captcha(soup):
    # get captcha from the html
    try:
        scripts = soup.find_all('script')
        res = ''
        for script in scripts:
            s = script.string
            if s is None:
                continue
            indx = s.find("ctl00_ctl00_ctl00_ctl07_captchaAnswer")
            if indx != -1:
                x1 = s.find('=', indx)
                x2 = s.find(';', indx)
                res = s[x1 + 1:x2].strip().replace("'", "")
        return res
    except Exception as e:
        print(e)


def get_criminal_record(soup):
    # get details from html
    try:
        data_table = soup.find("table", class_="gridView")
        if data_table:
            tr = data_table.find("tr", class_="gridViewRow")
            all_tds = tr.find_all("td")
            if all_tds:
                json_out = {
                "docket_number": all_tds[7].text.strip(),
                "court_office" : all_tds[8].text.strip(),
                "short_caption": all_tds[9].text.strip(),
                "filling_date": all_tds[10].text.strip(),
                "country": all_tds[11].text.strip(),
                "case_status": all_tds[12].text.strip(),
                "primary_participant": all_tds[13].text.strip(),
                "OTN" : all_tds[15].text.strip(),
                "complaint_number": all_tds[18].text.strip(),
                "police_incident": all_tds[18].text.strip(),
                "date_of_birth": all_tds[19].text.strip()
            }

            return json.dumps(json_out)
        return False
    except Exception as e:
        print(e)


def fetching_records(self,*args,**kwargs):
    # fetching data from the url 
    headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.17 (KHTML, like Gecko)  Chrome/24.0.1312.57 Safari/537.17',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'en-US,en;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3'
    }

    with requests.Session() as session:
        session.headers = headers

        URL = "https://ujsportal.pacourts.us/DocketSheets/MDJ.aspx"
        print(URL)

        res1 = session.get(URL, headers=headers)
        
        soup = BeautifulSoup(res1.content,'html.parser')

        captcha_answer = find_captcha(soup)



        data = {
                    "__EVENTTARGET": "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$ddlSearchType",
                    "__EVENTARGUMENT": "",
                    "__LASTFOCUS" : "",
                    "__SCROLLPOSITIONX": soup.find("input", attrs={'name': '__SCROLLPOSITIONX'}).get("value"),
                    "__SCROLLPOSITIONY": soup.find("input", attrs={'name': '__SCROLLPOSITIONY'}).get("value"),
                    "__VIEWSTATE": soup.find("input", attrs={'name': '__VIEWSTATE'}).get("value"),
                    "__VIEWSTATEGENERATOR": soup.find("input", attrs={'name': '__VIEWSTATEGENERATOR'}).get("value"),
                    "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$ddlSearchType": "ParticipantName",
                    "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsDocketNumber$ddlCounty": '',
                    "ctl00$ctl00$ctl00$ctl07$captchaAnswer": captcha_answer
                }

        res = session.post(URL,headers=headers, data=data)
        cookies = res.cookies
        soup1 = BeautifulSoup(res.content, "html.parser")

        captcha_answer1 = find_captcha(soup1)

        payload = {
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS" : "",
            "__SCROLLPOSITIONX": soup1.find("input", attrs={'name': '__SCROLLPOSITIONX'}).get("value"),
            "__SCROLLPOSITIONY": soup1.find("input", attrs={'name': '__SCROLLPOSITIONY'}).get("value"),
            "__VIEWSTATE": soup1.find("input", attrs={'name': '__VIEWSTATE'}).get("value"),
            "__VIEWSTATEGENERATOR": soup1.find("input", attrs={'name': '__VIEWSTATEGENERATOR'}).get("value"),
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$ddlSearchType": "ParticipantName",
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$txtLastName" : query_parms['last_name'],
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$txtFirstName": query_parms['first_name'],
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$dpDOB$DateTextBox": query_parms['date_of_birth'],
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$dpDOB$DateTextBoxMaskExtender_ClientState": "",
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$ddlCounty": "",
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$ddlDocketType": "CR",
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$ddlCaseStatus": "",
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$DateFiledDateRangePicker$beginDateChildControl$DateTextBox": "__/__/____",
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$DateFiledDateRangePicker$beginDateChildControl$DateTextBoxMaskExtender_ClientState": "",
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$DateFiledDateRangePicker$endDateChildControl$DateTextBox": "__/__/____",
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$cphSearchControls$udsParticipantName$DateFiledDateRangePicker$endDateChildControl$DateTextBoxMaskExtender_ClientState": "",
            "ctl00$ctl00$ctl00$cphMain$cphDynamicContent$btnSearch" : "Search",
            "ctl00$ctl00$ctl00$ctl07$captchaAnswer": captcha_answer1
        }
        
        res2 = session.post(URL,headers=headers,data=payload,cookies=cookies)
        res2_result = BeautifulSoup(res2.text, "html.parser")
        result = get_criminal_record(res2_result)
    return result

query_parms = {
    'last_name':'rios',
    'first_name':'william',
    'date_of_birth':'07/31/1975'
}


check_records = fetching_records(query_parms)

if check_records:
    print(check_records)
else:
    print('No records found')