import requests
from bs4 import BeautifulSoup
from hashlib import md5
import json
import time



upgrade = {}

file_name = "history.txt"
log_name = "log.txt"
base_local = "base.json"
sent_type = ""
aggent_id = 0
corp_secret = ""
corp_id = ""
user_id = ""
boss_id = ""

def find_content(url):
    header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36','Connection': 'close'}
    res = requests.get(url,headers = header)
    res.encoding = 'utf-8'
    return res.text

def create_md5(content):
    new_md5 = md5()
    new_md5.update(content.encode(encoding='utf-8'))
    md5_digest = new_md5.hexdigest()
    return md5_digest

def send_message(_message,user_id,server_url): # 默认发送给自己

    if sent_type == "Server":
        response = requests.get(f'{server_url}?title=追的小说更新啦&desp={_message}')
        data = json.loads(response.text)
        return data["data"]["error"] == "SUCCESS"

    response = requests.get(f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={corp_secret}")
    data = json.loads(response.text)
    access_token = data['access_token']

    json_dict = {
       "touser" : user_id,
       "msgtype" : "text",
       "agentid" : aggent_id,
       "text" : {
           "content" : _message
       },
       "safe": 0,
       "enable_id_trans": 0,
       "enable_duplicate_check": 0,
       "duplicate_check_interval": 1800
    }
    json_str = json.dumps(json_dict)
    response_send = requests.post(f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}", data=json_str)
    return json.loads(response_send.text)['errmsg'] == 'ok'

def bi_qu_ge(url):
    change = {}
    text = find_content(url)
    soup = BeautifulSoup(text, features="lxml")
    update = soup.find('div', id="info").find("a", attrs={"target": "_blank"})
    title_md5 = create_md5(update.text)
    change["md5"] = title_md5
    base_url = 'https://www.biduoxs.com'
    content_url = base_url + update['href']
    change["url"] = content_url
    fiction_content = find_content(content_url)
    fiction = BeautifulSoup(fiction_content,features="lxml")
    content = fiction.find("div",id="content")
    change["ready"] = len(content) > 100
    return change

def shu_qu_ge(url):
    change = {}
    text = find_content(url)
    soup = BeautifulSoup(text, features="lxml")
    update = soup.find('div', class_="block_txt2").find_all('a')
    last = None
    for last in update:pass
    base_url = 'https://wap.shuquge.com'
    content_url = base_url + last['href']
    change["url"] = content_url
    fiction_content = find_content(content_url)
    fiction = BeautifulSoup(fiction_content, features="lxml")
    content = fiction.find("div", id="nr1")
    change["ready"] = len(content) > 100
    return change

def query_new_chapter(url,type):
    if type == "biqu":
        return bi_qu_ge(url)
    elif type == "shuqu":
        return shu_qu_ge(url)


def history_record(change,origin_type,taget_id):
    url = change.get("url")
    ready = change.get("ready")
    name = change.get("name")

    if upgrade.get(taget_id) is None:
        upgrade[taget_id] = {}
        upgrade[taget_id][origin_type] = {}
    if upgrade.get(taget_id).get(origin_type) is None:
        upgrade[taget_id][origin_type] = {}

    exist_url = upgrade.get(taget_id).get(origin_type).get(name)

    if exist_url is None:
        upgrade[taget_id][origin_type][name] = url
        return False

    if exist_url != url:
        if ready:
            upgrade[taget_id][origin_type][name] = url
            return True
    return False



def do_log(change_list,message=None):
    with open(log_name,"a") as f:
        f.write(time.asctime(time.localtime(time.time())) + "\n")
        for change in change_list:
            f.write(str(change) + "\n")
        if message is not None:
            f.write(message)
        f.write("dic -> " + str(upgrade) + "\n")
        f.flush()

def init_data():
    global aggent_id
    global corp_secret
    global corp_id
    global boss_id
    global sent_type
    global server_url
    with open(base_local,"r",encoding='UTF-8') as f:
        load_dic = dict(json.load(f))
        aggent_id = load_dic.get("aggent_id")
        corp_secret = load_dic.get("corp_secret")
        corp_id = load_dic.get("corp_id")
        boss_id = load_dic.get("boss_id")
        sent_type = load_dic.get("send_type")
        return load_dic.get("data")

def check_update_ready():
    change_list = []
    data = init_data()
    for user in data:
        origin = user.get("base")
        taget_id = user.get("user_id")
        server_url = user.get("server_url")
        for origin_type,v in origin.items():
            # print("源：" + str(upgrade))
            for name,url in v.items():
                change = query_new_chapter(url, origin_type)
                change["name"] = name
                need = history_record(change,origin_type,taget_id)
                change["need"] = need
                if change.get("ready") == True and need == True:
                    message = name + "更新：" + change.get("url")
                    # print("发送给：" + taget_id + "内容为：" + message)
                    send_message(message,taget_id)
                    do_log([],message)
                change_list.append(change)
            # print("后：" + str(upgrade))
    do_log(change_list)

def monitor():
    error = False
    while True:
        try:
            check_update_ready()
            error = False
        except Exception as e:
            if not error:
                send_message(str(e),boss_id)
                error = True
        time.sleep(300)


if __name__ == '__main__':
    monitor()
