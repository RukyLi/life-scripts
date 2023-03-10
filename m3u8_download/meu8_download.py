# coding=gbk
import os

import requests




headers = {

            'Connection': 'Keep-Alive',

            'Accept': 'application/vnd.apple.mpegurl',

            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'

        }


class IndexM3U8():

    def __init__(self,url):
        self.url = url

    def resolve_index(self):
        ts_list = []
        m3u8_index_content = requests.get(self.url,headers)
        for item in m3u8_index_content.text.split(",")[1:]:
            ts_list.append(item.split("#")[0].strip("\n"))
        return ts_list


class DownloadTs():

    def __init__(self,ts_index,base_url):
        self.ts_index = ts_index
        self.base_url = base_url
        self.store_dir = "D:\\mdx(107部全集)\\test\\"

    def download_ts(self):
        for ts in self.ts_index:
            download_ts_url = self.base_url + "/" + ts
            path = self.store_dir + ts
            if os.path.isfile(path):
                print(ts + "分片已存在跳过下载")
                continue
            print("开始下载分片:" + ts)
            resp = requests.get(download_ts_url,headers)
            print("分片：" + ts + "下载完成")
            with open(path,'wb') as f:
                f.write(resp.content)



    # def merge(self):
    #     merge_list = os.listdir("D:\\mdx(107部全集)\\test")
    #     merge_list.sort(key=lambda x: int(x.split('.')[0]))
    #     with open("D:\\mdx(107部全集)\\kk.ts",'a',encoding='utf-8') as f:
    #         for item in merge_list:
    #             with open("D:\\mdx(107部全集)\\test\\" + item,'r',encoding='utf-8') as k:
    #                 f.write(k.read())
    #                 print("合并分片：" + item + "完成")




        # abc = 'copy /b D:\\mdx(107部全集)\\test\\*.ts D:\\mdx(107部全集)\\wxx.mp4'
        # os.system(abc)


if __name__ == '__main__':
    aa = IndexM3U8('https://t21.cdn2020.com/video/m3u8/2023/02/05/05bf6d9e/index.m3u8')
    ts_list = aa.resolve_index()
    bb = DownloadTs(ts_list,'https://t21.cdn2020.com/video/m3u8/2023/02/05/05bf6d9e')
    # bb.download_ts_2()
