# oshwhub_autosign
~~利用github action实现~~已魔改至腾讯云函数实现并添加 Telegram Bot 通知支持的立创 oshwhub 社区自动登录+自动签到+自动领取三天及七天签到奖励脚本, 支持多用户签到

# 食用方法
修改源代码第360行之后的内容，添加自己的 OSHWHub 登录账号和密码，以及推送相关的各类信息。
若需要在腾讯云云函数上部署，请 clone 本仓库后使用 pip3 执行下列命令以安装依赖并修改配置：
```
pip install BeautifulSoup4 -t oshwhub_autosign/
```
再打包部署至腾讯云上，执行器为main_handler。
# 以下为原作者提供的内容
# action体验不佳, 不再直接支持action, 请自行fork修改 
# ~~建议还是部署在自己本地的树莓派或者装了python的op路由器之类的上面哈, action不太稳的样子~~

~~以下是action食用方式~~
1. ~~右上角fork本仓库~~
2. ~~点击Settings -> Secrets -> 点击绿色按钮 (如无绿色按钮说明已激活。直接到第三步。)~~
3. ~~新增 一个secret, Name 为`OSHW`, value为如下json样式:~~
```
{"手机号1":"密码1","手机号2":"密码2",...,"手机号n":"密码n"}
```
![图片](https://github.com/seishinkouki/oshwhub_autosign/blob/main/Snipaste_2021-04-24_13-44-31.png)

4. ~~点击右上角自己仓库的Star可以触发运行，也可以在action中手动run, 同时会定时在每天的0:10, 1:10, 2:10自动运行, 三次应该能够百分百成功了, 如果想改为其它时间自行修改corn~~
5. ~~**必须** - 请随便找个文件(例如`README.md`)，加个空格提交一下，否则可能会出现无法定时执行的问题~~
  
