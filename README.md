# life-scripts
划水时候写的一些脚本，刚学习python，工作语言还是java

如果是初学者不会的可以发邮件给我 729365796@qq.com 大佬们源码就能看懂，不满意的话可以diy，别diss我，边学边写的，工作划水图个乐

## fiction_update_notice

#### 小说更新微信消息通知脚本

作用：在你看的小说更新之后会自动发消息到你的微信并附上链接提醒你小说更新了

+ 支持的盗版小说网址：书趣阁和笔趣阁

+ 支持的推送方式：Server酱推送，企业微信推送(可以微信扫码企业微信插件转通知到微信，企业微信可卸载)

**Server酱推送方式**：

```json
// 文件名为 base.json，放在find_data.py同一个目录下面
{
    "send_type": "Server", // 类型指定必须加，server酱模式写的就是Server
    "data": [ // 可支持多个用户分别通知各自的小说更新情况
        {
            "server_url": "https://sctapi.ftqq.com/{sendkey}.send", // Server酱上获取的sendkey填充进去就行
            "user_id": "用户id1", // Server酱模式下随便命名就好了
            "base": {
                "shuqu": { // shuqu是类型指定，shuqu表示采取书趣阁的源，最好用这个，换源的话 需要自己修改
                    "夜的命名术": "https://wap.shuquge.com/s/3478.html", // 对应小说名字以及小说的首页url
                    "轮回乐园": "https://wap.shuquge.com/s/73988.html",
                    "恐怖复苏": "https://wap.shuquge.com/s/83354.html"
                }
            }
        },
        {
            "server_url": "https://sctapi.ftqq.com/{sendkey}.send",
            "user_id": "用户id2",
            "base": {
                "shuqu": {
                    "恐怖复苏": "https://wap.shuquge.com/s/83354.html"
                }
            }
        }

    ]
}
```

**sendkey获取方式**

1. 登陆Server酱：https://sct.ftqq.com/login

2. 扫码获取key

3. 复制sendkey

   ![](http://bubble.seahubn.cn/mk/server2.jpg)

   ![](http://bubble.seahubn.cn/mk/server1.jpg)

填充到上面的{sendkey}，配置文件便已经准备完成

**企业微信转微信推送方式**：

1. 注册企业微信

2. 获取账号相关密钥

3. 填充指定参数

   ```json
   {
       "boss_id": "用户id", // 这个用处是在系统之后指定将错误信息推送给谁
       "aggent_id": 应用id,
       "corp_secret": "应用secret",
       "corp_id": "企业id", 
       "data": [
   
           {
               "user_id": "需要推送的用户id",
               "base": {
                   "shuqu": {
                       "夜的命名术": "https://wap.shuquge.com/s/3478.html",
                       "轮回乐园": "https://wap.shuquge.com/s/73988.html",
                       "恐怖复苏": "https://wap.shuquge.com/s/83354.html"
                   }
               }
           },
           {
               "user_id": "需要推送的用户id",
               "base": {
                   "shuqu": {
                       "从木叶开始逃亡": "https://wap.shuquge.com/s/134509.html"
                   }
               }
           }
   
       ]
   }
   ```

   **企业注册方式**   参考[这里](https://blog.csdn.net/qq_29300341/article/details/115560813)的方案三

   1. 用电脑打开[企业微信官网](https://work.weixin.qq.com/)，注册一个企业

   2. 注册成功后，点「管理企业」进入管理界面，选择「应用管理」 → 「自建」 → 「创建应用」

      应用名称填入「鹏鹏的忠实粉丝」（此处可以用自己喜欢的名字），可见范围选择公司名。

      ![](http://bubble.seahubn.cn/mk/qywx1.png)
   
   3. 创建完成后进入应用详情页，可以得到`应用ID( agentid )`，`应用Secret( secret )`。对应aggent_id和corp_secret
   
      ![](http://bubble.seahubn.cn/mk/qywx2.png)
   
   4. 第三步，获取企业ID,进入「我的企业」页面，拉到最下边，可以看到`企业ID`。对应corp_id
   
   5. 进入「通讯录」页面，再点击自己的名字，可以看到`账号（即为userid）`。对应user_id或者boss_id
   
      ![](http://bubble.seahubn.cn/mk/qywx3.png)
   
      ![](http://bubble.seahubn.cn/mk/qywx4.png)
   
   6. 推送消息到微信,进入「我的企业」 → 「微信插件」，拉到下边扫描二维码，关注以后即可收到推送的消息。
   
     有可能会出现，发送成功，但是手机微信无法收到消息的情况，如何解决？

**服务器安装**：可以[参考这里](https://blog.csdn.net/qq_36441027/article/details/111182378)

+ 目前代码拉下来会有三个文件，分别是base.json即上面讲的两种配置方式二选一，find_data.py程序本体,requirement.txt安装列表

+ 代码拉下来之后三个文件放在一个目录下面

+ 服务器安装好python环境，可[参考这里](https://cloud.tencent.com/developer/article/1693084) 或者使用apt-get安装

+ 可以切到 /usr/local/下面创建scripts目录，将三个文件都放到该目录下面

+ 创建虚拟环境

  ```bash
  #安装虚拟环境
  pip3 install virtualenv
   
  # 创建python3.8版本的虚拟环境 venv
  virtualenv venv --python=python3.8
   
  # 切换到虚拟环境所在的目录
  cd venv
   
  # 启用虚拟环境
  source ./bin/activate 【1、退出虚拟环境:deactivate 2、删除虚拟环境:rm -r venv】
  
  #拉取文件进来
  cp ../base.json ../requirements.txt ../find_data.py ./
   
  # 安装依赖清单里的库
  pip3 install -r requirements.txt
   
  # 列出当前虚拟环境所安装的依赖库
  pip3 list
  ```

+ 启动python程序

  ```bash
  # 在后台启动xxx.py
  python find_data.py &
  ```

程序默认5分钟检查一次
