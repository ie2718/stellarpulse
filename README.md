# StellarPulse

> 🌟 星脉 —— AI驱动的科技情报监控系统 | 专注AI、具身智能、航天领域

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

StellarPulse（星脉）是一个智能科技情报监控系统，自动采集、分析并推送 AI、具身智能、航天等领域的最新资讯。

> 💫 来自星辰的脉动，捕捉科技前沿每一丝波动

## ✨ 核心功能

### 📡 多源数据采集
- RSS 订阅：机器之心、Solidot、36氪、量子位等
- API 接口：HackerNews、Reddit、arXiv
- 实时抓取：支持自定义数据源扩展

### 🧠 AI 智能分析
- 自动摘要生成
- 关键词提取
- 重要性评分 ⭐
- 内容情感分析
- 智能分类（AI/机器人/航天）

### 💬 交互式聊天查询
- WhatsApp/Telegram 命令交互
- 分类浏览：`/ai` `/robot` `/space`
- 关键词搜索：`/search GPT-5`
- 热门排行：`/hot`
- 详情查看：回复数字 1-8

### 🔔 关键词订阅
- 自定义关注词订阅
- 命中自动推送通知
- Web 界面管理订阅

### 🌐 Web 管理界面
- 实时资讯流展示
- 数据统计分析
- 历史报告查看
- 订阅管理

### 📱 多渠道推送
- WhatsApp 每日日报
- 关键词命中即时通知
- 可扩展邮件/Slack等

## 🚀 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/yourusername/stellarpulse.git
cd stellarpulse

# 安装依赖（Python 3.8+）
pip3 install -r requirements.txt

# 配置
cp config.example.json config.json
# 编辑 config.json 添加你的配置
```

### 运行

```bash
# 运行监控（单次）
python3 monitor.py

# 启动 Web 界面
python3 monitor.py --web
# 访问 http://localhost:8080

# 添加关键词订阅
python3 monitor.py --subscribe "SpaceX"
python3 monitor.py --list-subs
```

### 💬 聊天命令

在 WhatsApp/Telegram 发送：

```
/ai     - AI & 大模型资讯
/robot  - 机器人 & 具身智能
/space  - 航天 & 太空
/hot    - 热门 TOP 5
/latest - 最新 5 条
/search 关键词 - 全文搜索
/help   - 显示帮助
```

回复数字 `1-8` 查看详情

## 📁 项目结构

```
stellarpulse/
├── monitor.py              # 主程序入口
├── chat_bot.py             # 聊天交互入口
├── chat_handler.py         # 消息处理器
├── config.json             # 配置文件
├── data.json               # 数据存储
├── keywords.json           # 订阅存储
├── requirements.txt        # Python依赖
├── sources/                # 数据源模块
│   ├── __init__.py
│   ├── rss.py              # RSS源
│   ├── hackernews.py       # HackerNews
│   ├── reddit.py           # Reddit
│   ├── arxiv.py            # arXiv
│   ├── ai_summary.py       # AI摘要分析
│   └── subscription.py     # 订阅管理
├── web/                    # Web界面
│   └── server.py
└── reports/                # 生成的报告
```

## ⚙️ 配置说明

### config.json

```json
{
  "keywords": {
    "ai": ["AI", "大模型", "GPT", "神经网络"],
    "robotics": ["机器人", "具身智能", "机械臂"],
    "space": ["SpaceX", "航天", "卫星", "火箭"]
  },
  "sources": {
    "rss": [
      {"name": "机器之心", "url": "https://www.jiqizhixin.com/rss", "enabled": true}
    ],
    "api": [
      {"name": "HackerNews", "type": "hn", "enabled": true}
    ]
  },
  "settings": {
    "web_port": 8080,
    "items_per_category": 15,
    "enable_ai_summary": true
  }
}
```

### 定时任务（Crontab）

```bash
# 每天早上8点推送日报
0 8 * * * cd /path/to/stellarpulse && python3 monitor.py >> /var/log/stellarpulse.log 2>&1
```

## 🛠️ 数据源配置

### 启用 Reddit

编辑 `config.json`，将以下源 `enabled` 改为 `true`：
- Reddit-r-MachineLearning
- Reddit-r-robotics
- Reddit-r-space

### 启用 arXiv

- arXiv-AI (cs.AI)
- arXiv-Robotics (cs.RO)

## 📊 消息格式示例

**列表视图：**
```
🤖 AI & 大模型

1. 🤖 Vidu Q3 全球屠榜... ⭐⭐⭐
   机器之心 · 2小时前
2. 🤖 GLM-5架构曝光... ⭐⭐
   量子位 · 3小时前
...

💡 回复数字查看详情
```

**详情视图：**
```
📰 Vidu Q3 全球屠榜，击败马斯克xAI...
🏷️ 🤖 AI
📡 机器之心 · 2小时前

📝 AI视频生成模型Vidu Q3在全球评测中登顶...

🔗 https://www.jiqizhixin.com/...
```

## 🔧 开发计划

- [x] 多源数据采集
- [x] AI 智能分析
- [x] 关键词订阅
- [x] Web 管理界面
- [x] 聊天交互
- [ ] 邮件推送支持
- [ ] 更多数据源（Twitter/X）
- [ ] 数据可视化图表
- [ ] Docker 部署支持

## 🤝 贡献

欢迎提交 Issue 和 PR！

## 📄 License

MIT License © 2025
