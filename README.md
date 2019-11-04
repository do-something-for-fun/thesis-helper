# thesis-helper
毕业论文小助手：一个翻译英文并将中文结果显示在侧边的PDF阅读器  
2019.11.4下午，看英文论文，总是要在pdf阅读器和谷歌翻译之间来回折腾，好麻烦，想着能不能一个窗口解决问题，就有了下面这个程序。

### 效果图如下：
![效果图](./images/sample.png)

### 使用技术
1. PyQt5
2. pdfjs

### 使用说明
1. 把这个库里面的东西全下载到本地，然后再把目录下面的pdfjs-2.2.228-dist.zip解压一下
2. 再运行`pip install PyQt5, pyperclip, requests, json, uuid`，安装一些python的包
3. 再`python main.py`就启动了
