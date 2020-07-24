import requests

# response = requests.get("https://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_ cd=035720",  verify=False)
# print(response.text)

import requests
import re
import datetime

from bs4 import BeautifulSoup

def get_financial_statements(code):
    re_enc = re.compile("encparam: '(.*)'", re.IGNORECASE)
    re_id = re.compile("id: '([a-zA-Z0-9]*)' ?", re.IGNORECASE)

    #untrustful
    url = "https://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd={}".format(code)
    html = requests.get(url, verify=False).text
    encparam = re_enc.search(html).group(1)
    encid = re_id.search(html).group(1)

    url = "https://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd={}&fin_typ=0&freq_typ=A&encparam={}&id={}".format(
        code, encparam, encid)
    headers = {"Referer": "HACK"}
    html = requests.get(url, headers=headers, verify=False).text

    # #trustful
    # url = "https://finance.naver.com/item/main.nhn?code={}".format(code)
    # html = requests.get(url).text

    # print(html)

    soup = BeautifulSoup(html, 'html5lib')
    dividend = soup.select("table:nth-of-type(2) tr:nth-of-type(31) td span")
    years = soup.select("table:nth-of-type(2) th")

    # print(years[3:7])
    print(dividend)

    dividend_dict = {}
    for i in range(len(dividend)):
        dividend_dict[years[i+3].text.strip()[:4]] = dividend[i].text

    return dividend_dict

def get_3year_treasury():
    url = "http://www.index.go.kr/strata/jsp/showStblGams3.jsp?stts_cd=288401&amp;idx_cd=2884&amp;freq=Y&amp;period=1998:2016"
    html = requests.get(url, verify=False).text

    soup = BeautifulSoup(html, 'html5lib')
    td_data = soup.select("tr td")

    treasury_3year = {}
    start_year = 1998

    for x in td_data:
        treasury_3year[start_year] = x.text
        start_year +=1

    print(treasury_3year)
    return treasury_3year

    # print(type(td_data))
    # print(td_data[0].text)
    # print(td_data[1].text)
    # print(td_data[2].text)

def get_current_3year_treasury():
    url = "http://finance.naver.com/marketindex/interestDailyQuote.nhn?marketindexCd=IRR_GOVT03Y&page=1"
    html = requests.get(url).text

    soup = BeautifulSoup(html, 'html5lib')
    td_data = soup.select("tr td")

    return td_data[1].text

def get_dividend_yield(code):
    url = "http://companyinfo.stock.naver.com/company/c1010001.aspx?cmp_cd=" + code
    html = requests.get(url, verify=False).text

    soup = BeautifulSoup(html, 'html5lib')
    dt_data = soup.select("table.gHead03 tbody tr:nth-of-type(9) td")

    dividend_yield = dt_data[1].text[:4]

    # dividend_yield = dt_data[-2].text
    # dividend_yield = dividend_yield.split(' ')[1]
    # dividend_yield = dividend_yield[:-1]

    return dividend_yield

def get_previous_dividend_yield(code):
    dividend_yield = get_financial_statements(code)

    now = datetime.datetime.now()
    cur_year = now.year

    previous_dividend_yield = {}

    for year in range(cur_year-5, cur_year):
        if str(year) in dividend_yield.index:
            previous_dividend_yield[year] = dividend_yield[str(year)]

    return previous_dividend_yield

def get_estimated_dividend_yield(code):
    dividend_yield = get_financial_statements(code)
    dividend_yield = sorted(dividend_yield.items())[-1]

    return dividend_yield[1]

if __name__ == "__main__":
    # dividend_dict = get_financial_statements("035720")
    # get_3year_treasury()
    # print(get_current_3year_treasury())
    # print(dividend_dict)
    # dividend_yield = get_dividend_yield("058470")
    # print(dividend_yield)
    # print(get_previous_dividend_yield('058470'))

    # estimated_dividend_yield = get_estimated_dividend_yield('058470')
    # print(estimated_dividend_yield)