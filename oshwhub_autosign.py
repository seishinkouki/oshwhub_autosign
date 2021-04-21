import json
import re
import requests
import hashlib
import os


def cookies2dict(_cookies):
    _cookieDict = {}
    _cookies = _cookies.split("; ")
    for co in _cookies:
        co = co.strip()
        p = co.split('=')
        value = co.replace(p[0] + '=', '').replace('"', '')
        _cookieDict[p[0]] = value
    return _cookieDict


User_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 " \
             "Safari/537.36 "
cookies_Accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8," \
                 "application/signed-exchange;v=b3;q=0.9 "
oshw_url = "https://oshwhub.com"
oshw_res = requests.get(oshw_url)

# 后面需要用到acw_tc oshwhub_session oshwhubReferer
_oshw_cookies = cookies2dict(oshw_res.headers['Set-Cookie'])
print("未登录状态oshw网域的cookies:", _oshw_cookies)
# print(str(_oshw_cookies).replace("'", "").split(",")[4][17:])
_acw_tc = _oshw_cookies['acw_tc'].split(";")[0]
_oshwhub_session = str(_oshw_cookies).replace("'", "").split(",")[1][17:]
_oshwhubReferer = str(_oshw_cookies).replace("'", "").split(",")[4][17:]
# _CASAuth = _oshw_cookies['CASAuth']


oshw_headers = {
    "Accept": cookies_Accept,
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": requests.get(oshw_url).headers['Set-Cookie'],
    "Host": "oshwhub.com",
    "Pragma": "no-cache",
    "Referer": "https://oshwhub.com/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": User_Agent
}
oshw2passport_url = "https://oshwhub.com/login?from=https%3A%2F%2Foshwhub.com"
login_res = requests.get(oshw2passport_url, headers=oshw_headers, allow_redirects=False)
oshw2passport_cookies = cookies2dict(login_res.headers['Set-Cookie'])
print("跳转到PASSPORT过程中获取CASAuth:", oshw2passport_cookies['CASAuth'])

passport_headers = {
    "Accept": cookies_Accept,
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "passport.szlcsc.com",
    "Pragma": "no-cache",
    "Referer": "https://oshwhub.com/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": User_Agent
}
passport_res = requests.get(login_res.headers['Location'], headers=passport_headers, allow_redirects=False)
passport_cookies = cookies2dict(passport_res.headers['Set-Cookie'])
print("PASSPORT网域下acw_tc:", passport_cookies['acw_tc'])

passport_headers2 = {
    "Accept": cookies_Accept,
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": passport_res.headers['Set-Cookie'],
    "Host": "passport.szlcsc.com",
    "Pragma": "no-cache",
    "Referer": "https://oshwhub.com/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": User_Agent
}
passport_res = requests.get(passport_res.headers['Location'], headers=passport_headers2)
passport_cookies2 = cookies2dict(passport_res.headers['Set-Cookie'])
SSESION = passport_res.headers['Set-Cookie'].split(";")[-4].split("=")[-1]
print("获取新SSESION:", SSESION)

# print(passport_res.text)

LT = re.findall(r'<input type="hidden" name="lt" value="(.*?)" />', passport_res.text)
print("获取登录表单里lt参数:", LT[0])

login_url = "https://passport.szlcsc.com/login"
login_headers = {
    "Accept": cookies_Accept,
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Length": "373",
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "passport.szlcsc.com",
    "Origin": "https://passport.szlcsc.com",
    "Pragma": "no-cache",
    "Referer": "https://passport.szlcsc.com/login?service=https%3A%2F%2Foshwhub.com%2Flogin%3Ff%3Doshwhub",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": User_Agent
}
login_cookies = {
    "AGL_USER_ID": "247a99b7-7854-4c3e-8d47-92dc695f22c8",
    "fromWebSite": "oshwhub",
    "SESSION": SSESION
}
form_data = {
    "lt": LT[0],
    "execution": "e1s1",
    "_eventId": "submit",
    "loginUrl": "https://passport.szlcsc.com/login?service=https%3A%2F%2Foshwhub.com%2Flogin%3Ff%3Doshwhub",
    "afsId": "",
    "sig": "",
    "token": "",
    "scene": "login",
    "loginFromType": "shop",
    "showCheckCodeVal": "false",
    "pwdSource": "",
    "username": os.environ['phone'],
    "password": hashlib.md5(os.environ['passwd'].encode("utf8")).hexdigest(),
    "rememberPwd": "yes",
}
passport_res = requests.post(url=login_url, data=form_data, headers=login_headers, cookies=login_cookies,
                             allow_redirects=False)
print(passport_res.headers['Location'])
print(passport_res.headers['Set-Cookie'])
# print(passport_res.json)


# 验证ticket
oshw_headers = {
    "Accept": cookies_Accept,
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "oshwhub.com",
    "Pragma": "no-cache",
    "Referer": "https://passport.szlcsc.com/login?service=https%3A%2F%2Foshwhub.com%2Flogin%3Ff%3Doshwhub",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": User_Agent
}
oshw_cookies = {
    "acw_tc": _acw_tc,
    "oshwhubReferer": _oshwhubReferer,
    "oshwhub_session": _oshwhub_session,
    "CASAuth": oshw2passport_cookies['CASAuth']
}
# print(oshw_cookies['acw_tc'])
# print(oshw_cookies['oshwhubReferer'])
# print(oshw_cookies['oshwhub_session'])
# print(oshw_cookies['CASAuth'])

# print(oshw_cookies)
# 验证ticket
oshw_res = requests.get(passport_res.headers['Location'], headers=oshw_headers, cookies=oshw_cookies,
                        allow_redirects=False)
# print(oshw_res.headers['Location'])
# 更新session
oshw_res = requests.get(oshw_res.headers['Location'], headers=oshw_headers, cookies=oshw_cookies, allow_redirects=False)
oshw_cookies['oshwhub_session'] = cookies2dict(oshw_res.headers['Set-Cookie'])['oshwhub_session']
# print(oshw_res.headers['Set-Cookie'])
# print(oshw_cookies)

# 跳转oshw主页
oshw_res = requests.get(oshw_res.headers['Location'], headers=oshw_headers, cookies=oshw_cookies, allow_redirects=False)
oshw_cookies['oshwhub_session'] = cookies2dict(oshw_res.headers['Set-Cookie'])['oshwhub_session']
# print(oshw_cookies)

# 签到
# oshw_cookies = cookies2dict(oshw_res.headers['Set-Cookie'])
oshw_sign = requests.post("https://oshwhub.com/api/user/sign_in", headers=oshw_headers, cookies=oshw_cookies)
oshw_cookies['oshwhub_session'] = cookies2dict(oshw_res.headers['Set-Cookie'])['oshwhub_session']
# print(oshw_cookies)
print("签到结果:", json.loads(oshw_sign.content))

url_threeDay = "https://oshwhub.com/api/user/sign_in/getTreeDayGift"
url_sevenDay = "https://oshwhub.com/api/user/sign_in/getSevenDayGift"

# 获取三天签到奖励
oshw_res = requests.get(url_threeDay, headers=oshw_headers, cookies=oshw_cookies)
oshw_cookies['oshwhub_session'] = cookies2dict(oshw_res.headers['Set-Cookie'])['oshwhub_session']
# print(oshw_cookies)
print("三天奖励结果:", json.loads(oshw_res.content))

# 获取七日奖品信息
oshw_res = requests.get("https://oshwhub.com/api/user/sign_in/getUnbrokenGiftInfo", headers=oshw_headers,
                        cookies=oshw_cookies)
oshw_cookies['oshwhub_session'] = cookies2dict(oshw_res.headers['Set-Cookie'])['oshwhub_session']
print("七天奖品信息:", json.loads(oshw_res.content))
uuid = json.loads(oshw_res.content)['result']['sevenDay']['uuid']
coupon_uuid = json.loads(oshw_res.content)['result']['sevenDay']['coupon_uuid']

coupon_data = {
    "gift_uuid": uuid,
    "coupon_uuid": coupon_uuid
}
# 领取七日奖励
oshw_res = requests.post(url_sevenDay, data=coupon_data, headers=oshw_headers, cookies=oshw_cookies)
print("七天奖励结果:", json.loads(oshw_res.content))
