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


class Oshwhub:
    sign_Statistics = ""
    three_reward_Statistics = ""
    seven_reward_Statistics = ""
    User_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Chrome/86.0.4240.198 Safari/537.36 "
    cookies_Accept = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng," \
                     "*/*;q=0.8,application/signed-exchange;v=b3;q=0.9 "
    url_oshw = "https://oshwhub.com"
    url_oshw2passport = "https://oshwhub.com/login?from=https%3A%2F%2Foshwhub.com"
    url_login = "https://passport.szlcsc.com/login"
    url_signIn = "https://oshwhub.com/api/user/sign_in"
    url_threeDay = "https://oshwhub.com/api/user/sign_in/getTreeDayGift"
    url_sevenDay = "https://oshwhub.com/api/user/sign_in/getSevenDayGift"
    url_giftInfo = "https://oshwhub.com/api/user/sign_in/getUnbrokenGiftInfo"

    def __init__(self, phone, passwd):
        self.phone = phone
        self.passwd = passwd

    def auto_sign(self):
        oshw_res = requests.get(self.url_oshw)

        # 后面需要用到acw_tc oshwhub_session oshwhubReferer
        _oshw_cookies = cookies2dict(oshw_res.headers['Set-Cookie'])
        # print("未登录状态oshw网域的cookies:", _oshw_cookies)
        print("开始获取未登录状态oshw cookies...")
        # print(str(_oshw_cookies).replace("'", "").split(",")[4][17:])
        _acw_tc = _oshw_cookies['acw_tc'].split(";")[0]
        _oshwhub_session = str(_oshw_cookies).replace("'", "").split(",")[1][17:]
        _oshwhubReferer = str(_oshw_cookies).replace("'", "").split(",")[4][17:]
        # _CASAuth = _oshw_cookies['CASAuth']

        oshw_headers = {
            "Accept": self.cookies_Accept,
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Cookie": requests.get(self.url_oshw).headers['Set-Cookie'],
            "Host": "oshwhub.com",
            "Pragma": "no-cache",
            "Referer": "https://oshwhub.com/",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": self.User_Agent
        }
        login_res = requests.get(self.url_oshw2passport, headers=oshw_headers, allow_redirects=False)
        oshw2passport_cookies = cookies2dict(login_res.headers['Set-Cookie'])
        # print("跳转到PASSPORT过程中获取CASAuth:", oshw2passport_cookies['CASAuth'])
        print("开始获取CASAuth...")

        passport_headers = {
            "Accept": self.cookies_Accept,
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
            "User-Agent": self.User_Agent
        }
        passport_res = requests.get(login_res.headers['Location'], headers=passport_headers, allow_redirects=False)
        # print("PASSPORT网域下acw_tc:", passport_cookies['acw_tc'])

        passport_headers2 = {
            "Accept": self.cookies_Accept,
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
            "User-Agent": self.User_Agent
        }
        passport_res = requests.get(passport_res.headers['Location'], headers=passport_headers2)
        SESSION = passport_res.headers['Set-Cookie'].split(";")[-4].split("=")[-1]
        # print("获取新SESSION:", SESSION)
        print("开始获取新SESSION...")

        # print(passport_res.text)

        LT = re.findall(r'<input type="hidden" name="lt" value="(.*?)" />', passport_res.text)
        # print("获取登录表单里lt参数:", LT[0])
        print("开始获取登录表单里lt参数:")

        login_headers = {
            "Accept": self.cookies_Accept,
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
            "User-Agent": self.User_Agent
        }
        login_cookies = {
            "AGL_USER_ID": "247a99b7-7854-4c3e-8d47-92dc695f22c8",
            "fromWebSite": "oshwhub",
            "SESSION": SESSION
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
            "username": self.phone,
            "password": hashlib.md5(self.passwd.encode('utf-8')).hexdigest(),
            "rememberPwd": "yes",
        }
        print("开始登陆...")
        try:
            passport_res = requests.post(self.url_login, data=form_data, headers=login_headers, cookies=login_cookies,
                                         allow_redirects=False)
        except KeyError:
            self.sign_Statistics = "签到结果: 登录失败, 可能原因1:用户密码错误2:登录需要验证"
            return
        # print(passport_res.headers['Location'])
        # print(passport_res.headers['Set-Cookie'])
        # print(passport_res.json)

        # 验证ticket
        oshw_headers = {
            "Accept": self.cookies_Accept,
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
            "User-Agent": self.User_Agent
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
        print("开始验证ticket...")
        try:
            oshw_res = requests.get(passport_res.headers['Location'], headers=oshw_headers, cookies=oshw_cookies,
                                    allow_redirects=False)
        except KeyError:
            self.sign_Statistics = "签到结果: 登录失败, 可能原因1:用户密码错误2:登录需要验证"
            return
        # print(oshw_res.headers['Location'])
        # 更新session
        print("更新SESSION...")
        oshw_res = requests.get(oshw_res.headers['Location'], headers=oshw_headers, cookies=oshw_cookies,
                                allow_redirects=False)
        oshw_cookies['oshwhub_session'] = cookies2dict(oshw_res.headers['Set-Cookie'])['oshwhub_session']
        # print(oshw_res.headers['Set-Cookie'])
        # print(oshw_cookies)

        # 跳转oshw主页
        oshw_res = requests.get(oshw_res.headers['Location'], headers=oshw_headers, cookies=oshw_cookies,
                                allow_redirects=False)
        oshw_cookies['oshwhub_session'] = cookies2dict(oshw_res.headers['Set-Cookie'])['oshwhub_session']
        # print(oshw_cookies)

        # 签到
        # oshw_cookies = cookies2dict(oshw_res.headers['Set-Cookie'])
        oshw_sign = requests.post(self.url_signIn, headers=oshw_headers, cookies=oshw_cookies)
        oshw_cookies['oshwhub_session'] = cookies2dict(oshw_res.headers['Set-Cookie'])['oshwhub_session']
        # print(oshw_cookies)
        # print("签到结果:", json.loads(oshw_sign.content))
        if not json.loads(oshw_sign.content)['code']:
            self.sign_Statistics = "签到结果: 签到成功"
        else:
            self.sign_Statistics = "签到结果: " + json.loads(oshw_sign.content)['message']
        # 获取三天签到奖励
        oshw_res = requests.get(self.url_threeDay, headers=oshw_headers, cookies=oshw_cookies)
        oshw_cookies['oshwhub_session'] = cookies2dict(oshw_res.headers['Set-Cookie'])['oshwhub_session']
        # print(oshw_cookies)
        # print("三天奖励结果:", json.loads(oshw_res.content))
        if not json.loads(oshw_res.content)['code']:
            self.three_reward_Statistics = "三天奖励领取结果: 领取成功"
        else:
            self.three_reward_Statistics = "三天奖励领取结果: " + json.loads(oshw_res.content)['message']

        # 获取七日奖品信息
        oshw_res = requests.get(self.url_giftInfo, headers=oshw_headers, cookies=oshw_cookies)
        oshw_cookies['oshwhub_session'] = cookies2dict(oshw_res.headers['Set-Cookie'])['oshwhub_session']
        # print("七天奖品信息:", json.loads(oshw_res.content))
        uuid = json.loads(oshw_res.content)['result']['sevenDay']['uuid']
        coupon_uuid = json.loads(oshw_res.content)['result']['sevenDay']['coupon_uuid']
        coupon_name = json.loads(oshw_res.content)['result']['sevenDay']['name']

        coupon_data = {
            "gift_uuid": uuid,
            "coupon_uuid": coupon_uuid
        }
        # 领取七日奖励
        oshw_res = requests.post(self.url_sevenDay, data=coupon_data, headers=oshw_headers, cookies=oshw_cookies)
        # print("七天奖励结果:", json.loads(oshw_res.content))
        if not json.loads(oshw_res.content)['code']:
            self.seven_reward_Statistics = "七天奖励领取成功, 奖品为: " + json.loads(oshw_res.content)['result']['info']
        else:
            self.seven_reward_Statistics = "七天奖励领取结果: " + json.loads(oshw_res.content)['message']


if __name__ == '__main__':
    try:
        users = json.loads(os.environ['oshw'])
    except json.decoder.JSONDecodeError:
        print("用户名密码解析失败, 请检查secret OSHW 的格式")
    else:
        print("需签到用户数量:", len(users))
        for key in users:
            print("开始用户" + key[:3] + "*******" + key[-2:] + "的签到...")
            my_user = Oshwhub(key, users[key])
            my_user.auto_sign()
            print(my_user.sign_Statistics)
            print(my_user.three_reward_Statistics)
            print(my_user.seven_reward_Statistics)
