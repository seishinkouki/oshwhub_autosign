# oshwhub_autosign
利用github action实现立创 oshwhub社区自动登录+自动签到+自动领取三天及七天签到奖励


<img src="https://github.com/seishinkouki/oshwhub_autosign/actions/workflows/python-app.yml/badge.svg?branch=main">


# 使用方式
1. 右上角fork本仓库
2. 点击Settings -> Secrets -> 点击绿色按钮 (如无绿色按钮说明已激活。直接到第三步。)
3. 新增 两个 secret 并设置key value, 一个secret为phone, 为你的手机号, 另一个secret为你的密码
![图片](https://github.com/seishinkouki/oshwhub_autosign/blob/main/Snipaste_2021-04-19_22-54-32.png)
4. 点击右上角自己仓库的Star可以触发运行，也可以在action中手动run, 同时会定时在每天的0:10, 1:10, 2:10自动运行, 三次应该能够百分百成功了, 如果想改为其它时间自行修改corn
5. **必须** - 请随便找个文件(例如`README.md`)，加个空格提交一下，否则可能会出现无法定时执行的问题
  
