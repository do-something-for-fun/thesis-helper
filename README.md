# thesis-helper
毕业论文小助手：一个翻译英文并将中文结果显示在侧边的PDF阅读器 。

2019.11.4下午，看英文论文，总是要在pdf阅读器和谷歌翻译之间来回折腾，好麻烦，想着能不能一个窗口解决问题，就有了下面这个程序。

## 效果图

![效果图](images/sample.png)

## 技术栈

+ `PyQt5`

+ `pdfjs`

## 使用方法

### Windows

1. 下载[压缩包](https://github.com/muhualing/thesis-helper/releases/download/v1.0/thesis-helper.zip)
2. 解压缩
3. 运行`thesis-helper.exe`
4. 把`pdf`拖拽进来
5. 选中要翻译的文本，右键复制，然后侧边栏就有中文翻译结果了

### Linux & Mac OS

至少需要有Python环境。

#### 有Git环境

命令行输入如下指令即可。

```shell
git clone git@github.com:QSCTech-Sange/thesis-helper.git
cd thesis-helper
pip install -r requirements.txt
python main.py
```

#### 无Git环境

1. 下载[压缩包](https://github.com/QSCTech-Sange/thesis-helper/archive/master.zip)

2. 解压缩
3. 进入解压缩的目录并在这个目录下打开一个控制台
4. 把`pdf`拖拽进来
5. 选中要翻译的文本，右键复制，然后侧边栏就有中文翻译结果了