import requests
from bs4 import BeautifulSoup
from hashlib import md5
import json
import time




base = {
    "shuqu_ydmms":{"夜的命名术":"https://wap.shuquge.com/s/3478.html"},
    "shuqu_lhly":{"轮回乐园":"https://wap.shuquge.com/s/73988.html"},
    "shuqu_kbfs":{"恐怖复苏":"https://wap.shuquge.com/s/83354.html"}
}

upgrade = {}

file_name = "history.txt"
log_name = "log.txt"

## 这是server酱的
# server_url = "https://sctapi.ftqq.com/SCT129842TTF3tOQ44d69Vc5A7LYzZZqBM.send"

## 应用id
aggent_id = 111
corp_secret = "应用secret"
corp_id = "企业id"
user_id = "用户id"

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

def send_message(_message): # 默认发送给自己

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
    print(update)
    title_md5 = create_md5(update.text)
    change["md5"] = title_md5
    base_url = 'https://www.biduoxs.com'
    content_url = base_url + update['href']
    change["url"] = content_url
    fiction_content = find_content(content_url)
    fiction = BeautifulSoup(fiction_content,features="lxml")
    content = fiction.find("div",id="content")
    change["ready"] = len(content) > 50
    print(change)
    return change

def shu_qu_ge(url):
    change = {}
    text = find_content(url)
    soup = BeautifulSoup(text, features="lxml")
    # print(soup)
    update = soup.find('div', class_="block_txt2").find_all('a')
    last = None
    for last in update:pass
    # print(last)
    base_url = 'https://wap.shuquge.com'
    content_url = base_url + last['href']
    # print(content_url)
    change["url"] = content_url
    fiction_content = find_content(content_url)
    fiction = BeautifulSoup(fiction_content, features="lxml")
    content = fiction.find("div", id="nr1")
    change["ready"] = len(content) > 50
    # print(change)
    return change

def query_new_chapter(url,type):
    origin = type.split("_")[0]
    if origin == "biqu":
        return bi_qu_ge(url)
    elif origin == "shuqu":
        return shu_qu_ge(url)


def history_record(change):
    url = change.get("url")
    ready = change.get("ready")
    name = change.get("name")

    exist_url = upgrade.get(name)

    if exist_url is None:
        upgrade[name] = url
        return False

    if exist_url != url:
        if ready:
            upgrade[name] = url
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


def check_update_ready():
    change_list = []
    for type in base:
        find = base.get(type)
        name = next(iter(find))
        change = query_new_chapter(find.get(name), type)
        # print(change)
        change["name"] = name
        need = history_record(change)
        change["need"] = need
        if change.get("ready") == True and need == True:
            message = name + "更新：" + change.get("url")
            send_message(message)
            do_log([],message)
        change_list.append(change)
    do_log(change_list)

def monitor():
    error = False
    while True:
        try:
            #print(upgrade)
            check_update_ready()
            error = False
            #print(upgrade)
        except Exception as e:
            if not error:
                send_message(str(e))
                error = True
        time.sleep(300)


if __name__ == '__main__':
    monitor()

