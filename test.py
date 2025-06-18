from datetime import datetime,date
from requests import get, post
from time import localtime
import json
import os
import random
import sys
import bs4
import requests
 
 
def get_weather():
    city_name = '仁寿'
    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.weather.com.cn',
        'Referer': 'http://www.weather.com.cn/weather1d/101271502.shtml',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.54'
    }
    
    try:
        url = "http://www.weather.com.cn/weather/101271502.shtml"
        response = get(url=url, headers=headers)
        response.encoding = 'utf-8'
        
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        
        # 存放日期
        list_day = []
        i = 0
        day_list = soup.find_all('h1')
        for each in day_list:
            if i <= 1:  # 今明两天的数据
                list_day.append(each.text.strip())
                i += 1
        
        # 天气情况
        list_weather = []
        weather_list = soup.find_all('p', class_='wea')
        for i in weather_list:
            list_weather.append(i.text.strip())
        list_weather = list_weather[0:2]  # 只取今明两天
        
        # 存放当前温度，和明天的最高温度和最低温度
        tem_list = soup.find_all('p', class_='tem')
        i = 0
        list_tem = []
        for each in tem_list:
            if i >= 0 and i < 2:
                try:
                    span_text = each.span.text.strip() if each.span else ""
                    i_text = each.i.text.strip() if each.i else ""
                    # 确保温度值为数字
                    span_text = span_text if span_text.replace('℃', '').isdigit() else "0"
                    i_text = i_text if i_text.replace('℃', '').isdigit() else "0℃"
                    list_tem.append([span_text, i_text])
                except AttributeError:
                    list_tem.append(["0", "0℃"])
                i += 1
        
        # 风力
        list_wind = []
        wind_list = soup.find_all('p', class_='win')
        for each in wind_list:
            try:
                wind_text = each.i.text.strip()
                list_wind.append(wind_text)
            except AttributeError:
                list_wind.append("无数据")
        list_wind = list_wind[0:2]  # 只取今明两天
        
        # 数据整理
        today_date = list_day[0]
        today_weather = list_weather[0]
        today_max = list_tem[0][0] + '℃' if not list_tem[0][0].endswith('℃') else list_tem[0][0]
        today_min = list_tem[0][1]
        today_wind = list_wind[0]
        
        tomorrow = list_day[1]
        tomorrow_weather = list_weather[1]
        tomorrow_max = list_tem[1][0] + '℃' if not list_tem[1][0].endswith('℃') else list_tem[1][0]
        tomorrow_min = list_tem[1][1]
        tomorrow_wind = list_wind[1]
        
        # 确保温度值都是有效的数字
        if not today_max.replace('℃', '').isdigit():
            today_max = "0℃"
        if not today_min.replace('℃', '').isdigit():
            today_min = "0℃"
        if not tomorrow_max.replace('℃', '').isdigit():
            tomorrow_max = "0℃"
        if not tomorrow_min.replace('℃', '').isdigit():
            tomorrow_min = "0℃"
        
        return (city_name, today_date, today_weather, today_min, today_max, 
                today_wind, tomorrow, tomorrow_weather, tomorrow_min, 
                tomorrow_max, tomorrow_wind)
                
    except Exception as e:
        print(f"获取天气数据失败: {e}")
        return None
 

def get_birthday(birthday, year, today):
    # 获取生日的月和日
    birthday_month = int(birthday.split("-")[1])
    birthday_day = int(birthday.split("-")[2])
    # 今年生日
    year_date = date(year, birthday_month, birthday_day)
    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today > year_date:
        birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = 0
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    return birth_day


def get_daily_love():
    # 每日一句情话
    url = "https://api.lovelive.tools/api/SweetNothings/Serialization/Json"
    r = requests.get(url)
    all_dict = json.loads(r.text)
    sentence = all_dict['returnObj'][0]
    daily_love = sentence
    return daily_love
 
 
def get_ciba():
    # 每日一句英语
    url = "http://open.iciba.com/dsapi/"
    r = get(url)
    note_en = r.json()["content"]
    note_ch = r.json()["note"]
    return note_ch, note_en
 
 
def get_color():
    # 往list中填喜欢的颜色即可
    color_list = ['#6495ED', '#3CB371']
    return random.choice(color_list)
 
 
def get_config():
    with open("config.json", "r") as f:
        config = json.load(f)
        return config
 
 
def get_token(config):
    url = "https://api.weixin.qq.com/cgi-bin/token"
    param = {
        "grant_type": "client_credential",
        "appid": config['appId'],
        "secret": config['appsecret']
    }
    response = requests.get(url=url, params=param)
    result = response.json().get("access_token")
    return result
 
 
def send_message(to_user, access_token, city_name, today_date, today_weather, today_max, today_min, today_wind,
                 tomorrow, tomorrow_weather, tomorrow_max, tomorrow_min, tomorrow_wind, daily_love, note_ch, note_en,
                 today_weather_str, today_str):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]
    # 获取在一起的日子的日期格式
    love_year = int(config["love_date"].split("-")[0])
    love_month = int(config["love_date"].split("-")[1])
    love_day = int(config["love_date"].split("-")[2])
    love_date = date(love_year, love_month, love_day)
    # 获取在一起的日期差
    love_days = str(today.__sub__(love_date)).split(" ")[0]
    # 获取所有生日数据
    birthdays = {}
    for k, v in config.items():
        if k[0:5] == "birth":
            birthdays[k] = v

    print(today_max, today_min)
 
    for i in to_user:
        data = {
            "touser": i,
            "template_id": config["templateId"],
            "url": "http://www.baidu.com",
            "topcolor": "#FF0000",
            "data": {
                "date": {
                    "value": "{} {}".format(today, week),
                    "color": get_color()
                },
                "city": {
                    "value": city_name,
                    "color": get_color()
                },
                "today": {
                    "value": today_date,
                    "color": get_color()
                },
                "today_weather": {
                    "value": today_weather,
                    "color": get_color()
                },
                "today_max": {
                    "value": today_max,
                    "color": get_color()
                },
                "today_min": {
                    "value": today_min,
                    "color": get_color()
                },
                "today_wind": {
                    "value": today_wind,
                    "color": get_color()
                },
                "tomorrow": {
                    "value": tomorrow,
                    "color": get_color()
                },
                "tomorrow_weather": {
                    "value": tomorrow_weather,
                    "color": get_color()
                },
                "tomorrow_max": {
                    "value": tomorrow_max,
                    "color": get_color()
                },
                "tomorrow_min": {
                    "value": tomorrow_min,
                    "color": get_color()
                },
                "tomorrow_wind": {
                    "value": tomorrow_wind,
                    "color": get_color()
                },
                "daily_love": {
                    "value": daily_love,
                    "color": get_color()
                },
                "birthday": {
                    "value": birthdays,
                    "color": get_color()
                },
                "love_day": {
                    "value": love_days,
                    "color": get_color()
                },
                "note_en": {
                    "value": note_en,
                    "color": get_color()
                },
                "note_ch": {
                    "value": note_ch,
                    "color": get_color()
                },
                "today_weather_str": {
                    "value": today_weather_str,
                    "color": get_color()
                },
                "today_str": {
                    "value": today_str,
                    "color": get_color()
                }
            }
        }
        for key, value in birthdays.items():
            # 获取距离下次生日的时间
            birth_day = get_birthday(value, year, today)
            # 将生日数据插入data
            data["data"][key] = {"value": birth_day, "color": get_color()}
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        response = post(url, headers=headers, json=data).json()
        if response["errcode"] == 40037:
            print("推送消息失败，请检查模板id是否正确")
        elif response["errcode"] == 40036:
            print("推送消息失败，请检查模板id是否为空")
        elif response["errcode"] == 40003:
            print("推送消息失败，请检查微信号是否正确")
        elif response["errcode"] == 0:
            print("推送消息成功")
        else:
            print(response)
 
 
if __name__ == "__main__":
    try:
        config = get_config()
    except FileNotFoundError:
        print("推送消息失败，请检查config.txt文件是否与程序位于同一路径")
        os.system("pause")
        sys.exit(1)
    except SyntaxError:
        print("推送消息失败，请检查配置文件格式是否正确")
        os.system("pause")
        sys.exit(1)
    # 获取accessToken
    accessToken = get_token(config)
    # 接收的用户
    users = config["userId"]
    # 传入省份和市获取天气信息
    city_name, today_date, today_weather, today_min, today_max, today_wind, tomorrow, tomorrow_weather, tomorrow_min, tomorrow_max, tomorrow_wind = get_weather()
    # 判断今天天气并返回对应响应
    # print(today_weather)
    today_weather_str = ""
    str_weather = ['雨', '云', '晴', '阴']
    # 提示可以多想几条 放入列表 random.choice([])
    today_weather_str_rain = ['今日可能有雨 记得带伞哦', '下雨天巧克力和音乐更配哦~', '天街小雨润如酥 草色遥看近却无',
                              '今日雨润如酥 记得带伞出门呀','听雨声潺潺 念你眉眼弯弯','雨打芭蕉 思念正好']
    today_weather_str_cloud = ['等风起，漫随天外云卷云舒', '今日有云 气候宜人', '应是天仙狂醉，乱把白云揉碎',
                               '云影摇曳 如诗如画','云淡风轻 愿你心情亦然',]
    today_weather_str_sun = ['快醒醒 太阳已经晒屁gu啦~', '今日天气晴 不止天气', '今天天气不错 多出门走走',
                             '阳光正好 微风不燥','风和日暖 岁月静好','阳光明媚 恰如你的笑眼','今日晴天，适合听《晴天》']
    today_weather_str_overcast = ['今日天气较阴 适宜懒人瘫在家里~', '阴天雨天暴雨天 爱你爱到发晒癫','阴天也是诗意的开始',
                                  '阴云遮日 也遮不住想你','阴天适合思念 也适合想你','阴天里藏着诗意 就像藏着对你的思念']
    for i in str_weather:
        if i in today_weather and i == '雨':
            today_weather_str = random.choice(today_weather_str_rain)
            break
        elif i in today_weather and i == '云':
            today_weather_str = random.choice(today_weather_str_cloud)
            break
        elif i in today_weather and i == '晴':
            today_weather_str = random.choice(today_weather_str_sun)
            break
        elif i in today_weather and i == '阴':
            today_weather_str = random.choice(today_weather_str_overcast)
            break
        else:
            today_weather_str = '啊哦 今天公众号有点不太聪明~ '
    # print(today_weather_str)
    # 判断今日温度并返回对应响应
    today_min_judge = today_min.split('℃')
    today_max_judge = today_max.split('℃')
    today_min_str = ''
    today_max_str = ''
    weather_min_str = ['今日温度较低 天冷记得加衣哦', '今日温度较低 要注意保暖哦','今日有些凉意 围巾手套记得带好',
                       '微凉的天最适合来杯暖暖的奶茶','天凉别着凉 加件外套再出门吧','今日微凉 记得添件外套呀']
    weather_max_str = ['今日温度较高 奖励自己一个冰淇淋降降温吧~', '今天好像比较热 记得防晒和消暑降温哦',
                       '今日温度有点高 记得防晒补水哦','天气炎热 记得避开正午外出哦','热天里奖励自己一个冰淇淋 甜到心里~']
    weather_center_str = ['今日温度适宜 适合运动练瑜伽~(doge)', '今日温度适宜 适合出去happy~','今日温度舒适宜人 不如出去拍些美美的照片']
    if int(today_min_judge[0]) < 10:
        today_str = random.choice(weather_min_str)
    elif int(today_max[0]) > 30:
        today_str = random.choice(weather_max_str)
    else:
        today_str = random.choice(weather_center_str)
    # print(today_str)
    # 获取每日情话.
    daily_love = get_daily_love()
    # 获取每日一句英语
    note_ch, note_en = get_ciba()
    # 公众号推送消息
    # 传入提醒信息
    send_message(users, accessToken, city_name, today_date, today_weather, today_max, today_min, today_wind,
                 tomorrow, tomorrow_weather, tomorrow_max, tomorrow_min, tomorrow_wind, daily_love, note_ch,
                 note_en, today_weather_str, today_str)
    # 这里系统暂停乱码 需要将pycharm设置成与cmd相同的GBK编码 在setting file encode中
    # os.system("pause")
