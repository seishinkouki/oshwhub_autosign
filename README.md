# oshwhub_autosign
利用github action实现立创 oshwhub社区自动登录+自动签到

# 使用方式
1. 右上角fork本仓库
2. 点击Settings -> Secrets -> 点击绿色按钮 (如无绿色按钮说明已激活。直接到第三步。)
3. 新增 两个 secret 并设置key value, 一个secret为phone, 为你的手机号, 另一个secret为你的密码的md5值, md5值可以在此网站计算[戳我](https://www.cmd5.com/hash.aspx?s=123456)
![网站](https://github.com/seishinkouki/oshwhub_autosign/blob/main/Snipaste_2021-04-19_22-46-32.png)
5. 点击右上角自己仓库的Star可以触发运行，也可以在action中手动run, 同时会定时在每天的0:10, 1:10, 2:10自动运行, 三次应该能够百分百成功了, 如果想改为其它时间自行修改corn
6. **必须** - 请随便找个文件(例如`README.md`)，加个空格提交一下，否则可能会出现无法定时执行的问题
  
