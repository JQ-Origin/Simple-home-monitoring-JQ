# Simple-home-monitoring-JQ
 

这个监控系统是一个基于 Flask 和 OpenCV 的简单应用，它允许用户通过连接到的 USB 摄像头实时查看视频，并支持视频录制和用户登录功能。

## 功能

+ 实时视频监控
+ 视频录制，每天自动保存为新文件
+ 用户登录界面
+ 安全退出功能
## 安装
确保您的系统已安装 Python 3。您还需要安装 Flask 和 OpenCV。这可以通过以下命令完成：

    pip install Flask opencv-python
#### 运行应用
克隆或下载此仓库到您的服务器。

    git clone https://github.com/JQ-Origin/Simple-home-monitoring-JQ.git

打开终端并切换到应用的目录。

    cd Simple-home-monitoring-JQ
运行以下命令来启动应用：

    python app.py
在浏览器中访问 http://<服务器地址>:<端口号(默认12971)> 来查看应用。

## 配置
所有的配置都存储在 config.py 文件中。您可以在这里设置以下参数：

+ USERNAME 和 PASSWORD: 登录凭据。
+ VIDEO_SAVE_PATH: 视频保存路径。
+ CAMERA_RESOLUTION: 摄像头分辨率。
确保根据您的环境和需求调整这些设置。

# 安全性和隐私
此系统较为简陋，请不要在公共或不安全的网络上暴露此监控系统。
定期检查和维护存储的视频文件。
# 许可
此项目根据 MIT 许可证发行。有关详细信息，请查看 LICENSE 文件。