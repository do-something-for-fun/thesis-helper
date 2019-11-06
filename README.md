# thesis-helper
毕业论文小助手：一个翻译英文并将中文结果显示在侧边的PDF阅读器 。

2019.11.4下午，看英文论文，总是要在pdf阅读器和谷歌翻译之间来回折腾，好麻烦，想着能不能一个窗口解决问题，就有了下面这个程序。

## 效果图

![效果图](sample/sample.png)

## 技术栈

+ `PyQt5` 用于GUI的实现
+ `pdfjs` 用于解析PDF
+ `微软翻译` 用于翻译

## 使用方法

### Windows

1. 下载[压缩包](https://github.com/muhualing/thesis-helper/releases/download/v1.0/thesis-helper.zip)（不是直接在本页面下载，要点击蓝色的链接，链接到release界面下载）
2. 解压缩
 `!!!此步骤务必保证解压后的文件夹在全英文路径下，中文路径会闪退`
3. 运行`thesis-helper.exe`
4. 把`pdf`拖拽进来
5. 选中要翻译的文本，右键复制，然后侧边栏就有中文翻译结果了

### Linux & Mac OS

至少需要有Python环境。

#### 有Git环境

命令行输入如下指令即可。

```shell
git clone git@github.com:muhualing/thesis-helper.git
cd thesis-helper
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
chmod a+x thesis-helper.py
./thesis-helper.py # or python thesis-helper.py
```

以后每次运行只需要双击`thesis-helper.py`即可。

你也可以给它创建快捷方式到任何你喜欢的地方。

#### 无Git环境

1. 下载[压缩包](https://github.com/QSCTech-Sange/thesis-helper/archive/master.zip)
2. 解压缩
3. 进入解压缩的目录并在这个目录下打开一个控制台
4. 控制台里执行`python thesis-helper.py`
5. 把`pdf`拖拽进来
6. 选中要翻译的文本，右键复制，然后侧边栏就有中文翻译结果了

### 致谢
感谢杨帅昊(QSCTech-Sange)、Jarvisss、Wye(Lucas-Wye)、dendenxu、qiqiph和ametake对`thesis-helper`做出的贡献(提交过 Issue 或者 PR)。

<a href="https://github.com/QSCTech-Sange">
    <img src="https://avatars1.githubusercontent.com/u/33112139?s=460&amp;v=4" width="50px">
</a> 
<a href="https://github.com/Jarvisss">
    <img src="https://avatars2.githubusercontent.com/u/16323003?s=400&v=4" width="50px">
</a> 
<a href="https://github.com/Lucas-Wye">
    <img src="https://avatars0.githubusercontent.com/u/30680577?s=400&v=4" width="50px">
</a> 
<a href="https://github.com/dendenxu">
    <img src="https://avatars0.githubusercontent.com/u/43734697?s=400&v=4" width="50px">
</a> 
<a href="https://github.com/qiqiph">
    <img src="https://avatars1.githubusercontent.com/u/37620794?s=400&v=4" width="50px">
</a> 
<a href="https://github.com/ametake">
    <img src="https://avatars2.githubusercontent.com/u/22291194?s=400&v=4" width="50px">
</a> 
