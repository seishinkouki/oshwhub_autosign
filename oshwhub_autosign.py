import json
import math
import random
import re
import time
import requests
import hashlib
import os
from bs4 import BeautifulSoup
from loguru import logger


def cookies2dict(_cookies):
    _cookieDict = {}
    _cookies = _cookies.split("; ")
    for co in _cookies:
        co = co.strip()
        p = co.split('=')
        value = co.replace(p[0] + '=', '').replace('"', '')
        _cookieDict[p[0]] = value
    return _cookieDict


def uuid_generator():
    uuid_pattern = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
    uuid = ""
    now_t = int(round(time.time() * 1000000)) / 1000.0
    for i in uuid_pattern:
        e = (int(now_t + 16 * random.random()) % 16) | 0
        now_t = math.floor(now_t / 16)
        if i != "-":
            uuid = uuid + hex(e if i == "x" else 3 & e | 8)[-1:]
        else:
            uuid = uuid + "-"
    # print(uuid)
    return uuid


def coolpush(token, msg):
    return json.loads(requests.post("https://push.xuthus.cc/send/" + token, data=msg).content)['message']


def weixinpush(corpid, corpsecret, agentid, msg):
    base_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?'
    req_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='
    data = {
        "touser": "@all",
        "toparty": "@all",
        "totag": "@all",
        "msgtype": "text",
        "agentid": agentid,
        "text": {
            "content": msg
        },
        "safe": 0,
        "enable_id_trans": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    data = json.dumps(data)
    urls = base_url + 'corpid=' + corpid + '&corpsecret=' + corpsecret
    resp = requests.get(urls).json()
    access_token = resp['access_token']
    req_urls = req_url + access_token
    res = requests.post(url=req_urls, data=data)
    return res.text


class Oshwhub:
    sign_Statistics = ""
    three_reward_Statistics = ""
    seven_reward_Statistics = ""
    sign_flag = 1
    three_reward_flag = 1
    seven_reward_flag = 1
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
        logger.info('开始获取未登录状态oshw cookies...')
        # print(str(_oshw_cookies).replace("'", "").split(",")[4][17:])
        _acw_tc = _oshw_cookies['acw_tc'].split(";")[0]
        _oshwhub_session = str(_oshw_cookies).replace("'", "").split(",")[1][17:]
        _oshwhubReferer = str(_oshw_cookies).replace("'", "").split(",")[4][17:]
        # _CASAuth = _oshw_cookies['CASAuth']

        oshw_headers = {
            "X-Forwarded-For": "8.8.8.8",
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
        logger.info('开始获取CASAuth...')

        passport_headers = {
            "X-Forwarded-For": "8.8.8.8",
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
            "X-Forwarded-For": "8.8.8.8",
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
        logger.info('开始获取新SESSION...')

        LT = re.findall(r'<input type="hidden" name="lt" value="(.*?)" />', passport_res.text)
        # print("获取登录表单里lt参数:", LT[0])
        logger.info('开始获取登录表单里lt参数...')

        login_headers = {
            "X-Forwarded-For": "8.8.8.8",
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
            "AGL_USER_ID": uuid_generator(),
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
        logger.info('开始登陆...')
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
            "X-Forwarded-For": "8.8.8.8",
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
        logger.info('开始验证ticket...')
        try:
            oshw_res = requests.get(passport_res.headers['Location'], headers=oshw_headers, cookies=oshw_cookies,
                                    allow_redirects=False)
        except KeyError:
            self.sign_Statistics = "签到结果: 登录失败, 可能原因1:用户密码错误2:登录需要验证"
            return
        # print(oshw_res.headers['Location'])
        # 更新session
        logger.info('更新SESSION...')
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
        # 签到状态检查
        # 获取签到页面
        soup = BeautifulSoup(
            requests.get("https://oshwhub.com/sign_in", headers=oshw_headers, cookies=oshw_cookies).text, "html.parser")

        for tag in soup.find_all("button", attrs={'class': "btn btn-secondary"}):
            if tag.get_text() == "已签到":
                self.sign_Statistics = "已签到过,取消签到"
                self.sign_flag = 0

        # oshw_cookies = cookies2dict(oshw_res.headers['Set-Cookie'])
        if self.sign_flag:
            oshw_sign = requests.post(self.url_signIn, headers=oshw_headers, cookies=oshw_cookies)
            oshw_cookies['oshwhub_session'] = cookies2dict(oshw_res.headers['Set-Cookie'])['oshwhub_session']
            # print(oshw_cookies)
            # print("签到结果:", json.loads(oshw_sign.content))
            if not json.loads(oshw_sign.content)['code']:
                self.sign_Statistics = "签到成功"
            else:
                self.sign_Statistics = json.loads(oshw_sign.content)['message']

        # 签到后刷新页面
        soup = BeautifulSoup(
            requests.get("https://oshwhub.com/sign_in", headers=oshw_headers, cookies=oshw_cookies).text, "html.parser")
        # 三天奖励状态
        for tag in soup.find_all("div", attrs={'class': "three-day"}):
            if tag.attrs['data-status'] == "0":
                self.three_reward_Statistics = "天数不够,取消领取"
                self.three_reward_flag = 0
            elif tag.attrs['data-status'] == "2":
                self.three_reward_Statistics = "已领取过,取消领取"
                self.three_reward_flag = 0

        if self.three_reward_flag:
            # 获取三天签到奖励
            oshw_res = requests.get(self.url_threeDay, headers=oshw_headers, cookies=oshw_cookies)
            oshw_cookies['oshwhub_session'] = cookies2dict(oshw_res.headers['Set-Cookie'])['oshwhub_session']
            # print(oshw_cookies)
            # print("三天奖励结果:", json.loads(oshw_res.content))
            if not json.loads(oshw_res.content)['code']:
                self.three_reward_Statistics = "三天奖励领取结果: 领取成功"
            else:
                # self.three_reward_Statistics = "三天奖励领取结果: " + json.loads(oshw_res.content)['message']
                self.three_reward_Statistics = json.loads(oshw_res.content)['message']

        # 七天奖励状态
        for tag in soup.find_all("div", attrs={'class': "seven-day"}):
            if tag.attrs['data-status'] == "0":
                self.seven_reward_Statistics = "天数不够,取消领取"
                self.seven_reward_flag = 0
            elif tag.attrs['data-status'] == "2":
                self.seven_reward_Statistics = "已领取过,取消领取"
                self.seven_reward_flag = 0

        if self.seven_reward_flag:
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
                # self.seven_reward_Statistics = "七天奖励领取结果: " + json.loads(oshw_res.content)['message']
                self.seven_reward_Statistics = json.loads(oshw_res.content)['message']


url_pushplus = "http://pushplus.hxtrip.com/send"

# 需修改部分
OSHW = '{"1300000": "123"}'

# 推送加 推送
# pushplus token
pushplus_token = ""

# qq酷推 推送
# coolpush token
coolpush_token = ""

# 微信推送
corpid = 'wwxxxx'  # 微信企业ID
corpsecret = 'abcdef'  # 企业微信应用的Secret
agentid = 00000000  # 企业微信应用的id
# ####

if __name__ == '__main__':
    try:
        users = json.loads(OSHW)
    except json.decoder.JSONDecodeError:
        logger.error('用户名密码解析失败, 请检查secret OSHW 的格式')
    else:
        logger.info("需签到用户数量: " + str(len(users)))
        for key in users:
            logger.info("开始用户" + key[:3] + "*******" + key[-2:] + "的签到...")
            my_user = Oshwhub(key, users[key])
            my_user.auto_sign()
            if '错误' in my_user.sign_Statistics:
                logger.error(my_user.sign_Statistics)
            else:
                logger.info(my_user.sign_Statistics)
            logger.info(my_user.three_reward_Statistics)
            logger.info(my_user.seven_reward_Statistics)
            Statistics_data = {
                "签到结果": my_user.sign_Statistics,
                "三天奖励结果": my_user.three_reward_Statistics,
                "七天奖励结果": my_user.seven_reward_Statistics
            }
            push_payload = {
                "token": pushplus_token,
                "title": "用户" + key[:3] + "*******" + key[-2:] + "签到结果",
                "content": str(Statistics_data),
                "template": "json"
            }

            coolpush_payload = key[:3] + "*******" + key[-2:] + "\r\n" + \
                               "签到结果: " + my_user.sign_Statistics + "\r\n" + \
                               "三天奖励结果: " + my_user.three_reward_Statistics + "\r\n" + \
                               "七天奖励结果: " + my_user.seven_reward_Statistics

            if my_user.sign_flag or my_user.three_reward_flag or my_user.seven_reward_flag:
                if len(coolpush_token) == 32:
                    logger.info('推送结果: ' + coolpush(coolpush_token, coolpush_payload.encode('UTF-8')))
                elif len(pushplus_token) == 32:
                    logger.info('推送结果: ' + json.loads(requests.post(url_pushplus, data=push_payload).content)['data'])
                elif agentid != 0:
                    logger.info(
                        '推送结果: ' + json.loads(weixinpush(corpid, corpsecret, agentid, coolpush_payload))['errmsg'])
                else:
                    logger.warning('未设置推送类型')
            else:
                logger.info('未发生新任务,不进行推送')
    logger.info('==程序执行结束==')
