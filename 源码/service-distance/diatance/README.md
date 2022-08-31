## 测量物体距离的小程序

#### 结构：Android+Python

Python后端

​	打包：pyinstaller -F boot.exe(单个可执行文件)

​				**pyinstaller -F xxx.py -i xxx.ico **设置图标

​    可执行：boot.exe,如果网络超时，可尝试重启

​	使用控制台子系统执行（和黑框交互）

​	图片检测：计算图片中物体的边长

​	限制：物体为非白色、背景尽量为白色/黑色、减少不必要的反光、相机与物体间的距离为40-50cm。



Android与Python网络通信

​	IP+Port的一致

