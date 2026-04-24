# 安装指南

## 系统要求

- Python 3.8+
- Linux/macOS/Windows WSL

## 安装步骤

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/techmonitor.git
cd techmonitor
```

### 2. 创建虚拟环境（推荐）

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置

```bash
cp config.example.json config.json
# 编辑 config.json，根据需要调整
```

### 5. 测试运行

```bash
python3 monitor.py
```

## 系统服务设置（Linux）

创建 systemd 服务文件 `/etc/systemd/system/techmonitor.service`：

```ini
[Unit]
Description=StellarPulse
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/techmonitor
ExecStart=/path/to/techmonitor/venv/bin/python monitor.py
Restart=on-failure
RestartSec=60

[Install]
WantedBy=multi-user.target
```

启用服务：

```bash
sudo systemctl enable techmonitor
sudo systemctl start techmonitor
sudo systemctl status techmonitor
```
