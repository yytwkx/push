# Weather Push
一个基于 GitHub Actions 的每日天气自动推送程序

## 功能
- 每日自动推送天气信息（爬取官方实时数据）
- 自定义推送时间
- 可自定义纪念日

## 运行时间
每天早上 07:00自动推送

## 城市代码编号
https://blog.csdn.net/u013634862/article/details/44886769

## 微信公众平台网址
https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login

## 配置文件示例
确保config文件与主程序位于同一路径且正确配置必要参数
```json
{
  "appId": "your_app_id",
  "appsecret": "your_app_secret",
  "userId": "user_open_id",
  "templateId": "your_template_id",
  "love_date": "2024-01-01",
  "birthday": "2024-01-01"
}
