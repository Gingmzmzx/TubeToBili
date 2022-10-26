# TubeToBili
YouTube视频自动一键转载到Bilibili，带GUI界面

# 实现
本程序使用`python`编写，主要使用`biliup`和`pytube`编写，GUI使用`PyQt5`编写，所有ui文件均位于`/ui`目录  
  
# 使用
进入界面，填写YouTube视频地址和B站分区。（B站分区ID见[使用说明书](https://www.bilibili.com/read/cv18327205)  
Bilibili Cookie可以从浏览器获取，**建议使用[biliup-rs命令行工具](https://github.com/ForgQi/biliup-rs/)登陆，在生成的cookies.json中获取Cookie**  
  
下载/上传时，请注意：
- 从YouTube下载视频时，请尽量开启代理的`全局模式`
- 上传B站时，请尽量开启`规则模式（PAC模式）`
- 下载完成后，会有五秒间隔时间\n下载或上传失败后，三秒后会自动重试
  
# 二次开发
我们不提供需要的模块列表，您可以根据文件中的引用自行安装模块。  
  
打包时，请更改`main.spec`中的`a`中的`pathex`绝对地址，然后使用`pyinstaller main.spec`打包  
**请注意，`main.spec`中`block_cipher`使用`pyi_crypto.PyiBlockCipher`加密，需要额外安装`pycrypto`包，如果嫌麻烦直接把`block_cipher`赋值改成`None`即可！**   
  
# 开源协议
本仓库基于`Mozilla Public License 2.0`协议。  
- 您不能将本项目及二次开发的项目和衍生项目应用于商业范围；  
- 请您在二次开发项目中注明原作者版权信息
- 基于本项目的衍生项目和二次开发项目必须公开源代码