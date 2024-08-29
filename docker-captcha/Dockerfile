# 使用 Python 作为基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /docker

# 安装 Node.js 和 npm 以及 libGL.so.1 的依赖库
RUN apt-get update && \
    apt-get install -y curl libgl1-mesa-glx libglib2.0-0 && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# 设置国内镜像源（npm 和 pip）
RUN npm config set registry https://registry.npmmirror.com && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 复制应用代码到容器中
COPY . /docker

# 安装 Python 依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 初始化 npm 并安装 jsdom 模块
RUN npm init -y && \
    npm install jsdom

# 暴露应用端口
EXPOSE 6060

# 设置启动命令
CMD ["python3", "captcha.py"]

