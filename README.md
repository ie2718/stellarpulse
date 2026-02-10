<div align="center">

# 🌟 StellarPulse / 星脉

**AI-Powered Tech Intelligence Monitor**  
**AI 驱动的科技情报监控系统**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-2.0-orange.svg)]()

> *Pulse from the stars, capturing every ripple of tech frontier.*  
> *来自星辰的脉动，捕捉科技前沿每一丝波动。*

[English](#english) | [中文](#中文)

</div>

---

<a name="english"></a>
## 🇺🇸 English

### 📋 Overview

**StellarPulse** is an AI-powered tech intelligence monitoring system that automatically collects, analyzes, and delivers the latest news in AI, Embodied Intelligence, and Space exploration.

### ✨ Features

- **📡 Multi-Source Data Collection**
  - RSS feeds: 机器之心, Solidot, 36氪, 量子位
  - APIs: HackerNews, Reddit, arXiv, **X/Twitter**
  - Custom data source extensions supported

- **🧠 AI-Powered Analysis**
  - Automatic summarization
  - Keyword extraction
  - Importance scoring ⭐
  - Sentiment analysis
  - Smart categorization (AI/Robotics/Space)

- **💬 Interactive Chat Bot**
  - WhatsApp/Telegram command interface
  - Category browsing: `/ai` `/robot` `/space`
  - Keyword search: `/search GPT-5`
  - Hot trends: `/hot`
  - Detail view: Reply with numbers 1-8

- **🔔 Keyword Subscription**
  - Custom keyword subscriptions
  - Instant notifications on matches
  - Web interface management

- **🌐 Web Dashboard**
  - Real-time news stream
  - Data analytics
  - Historical reports
  - Subscription management

### 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/stellarpulse.git
cd stellarpulse

# Install dependencies (Python 3.8+)
pip3 install -r requirements.txt

# Configuration
cp config.example.json config.json
# Edit config.json to add your settings
```

### 💬 Chat Commands

Send these commands in WhatsApp/Telegram:

```
/ai     - AI & LLM news
/robot  - Robotics & Embodied AI
/space  - Space & Aerospace
/hot    - Top 5 trending
/latest - Latest 5 news
/search keyword - Full-text search
/help   - Show help
```

Reply with number `1-8` to view details.

### 📁 Project Structure

```
stellarpulse/
├── monitor.py              # Main entry
├── chat_bot.py             # Chat interface
├── config.json             # Configuration
├── sources/                # Data sources
│   ├── rss.py
│   ├── twitter.py          # X/Twitter API
│   ├── hackernews.py
│   └── ...
├── web/                    # Web dashboard
└── docs/                   # Documentation
```

---

<a name="中文"></a>
## 🇨🇳 中文

### 📋 项目简介

**星脉 (StellarPulse)** 是一个 AI 驱动的科技情报监控系统，自动采集、分析并推送 AI、具身智能、航天等领域的最新资讯。

### ✨ 核心功能

- **📡 多源数据采集**
  - RSS 订阅：机器之心、Solidot、36氪、量子位
  - API 接口：HackerNews、Reddit、arXiv、**X/Twitter**
  - 支持自定义数据源扩展

- **🧠 AI 智能分析**
  - 自动摘要生成
  - 关键词提取
  - 重要性评分 ⭐
  - 内容情感分析
  - 智能分类（AI/机器人/航天）

- **💬 交互式聊天查询**
  - WhatsApp/Telegram 命令交互
  - 分类浏览：`/ai` `/robot` `/space`
  - 关键词搜索：`/search GPT-5`
  - 热门排行：`/hot`
  - 详情查看：回复数字 1-8

- **🔔 关键词订阅**
  - 自定义关注词订阅
  - 命中自动推送通知
  - Web 界面管理订阅

- **🌐 Web 管理界面**
  - 实时资讯流展示
  - 数据统计分析
  - 历史报告查看
  - 订阅管理

### 🚀 快速开始

```bash
# 克隆仓库
git clone https://github.com/yourusername/stellarpulse.git
cd stellarpulse

# 安装依赖（Python 3.8+）
pip3 install -r requirements.txt

# 配置
cp config.example.json config.json
# 编辑 config.json 添加你的配置
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

回复数字 `1-8` 查看详情。

### 📁 项目结构

```
stellarpulse/
├── monitor.py              # 主程序入口
├── chat_bot.py             # 聊天交互入口
├── config.json             # 配置文件
├── sources/                # 数据源模块
│   ├── rss.py              # RSS源
│   ├── twitter.py          # X/Twitter API
│   ├── hackernews.py       # HackerNews
│   └── ...
├── web/                    # Web界面
└── docs/                   # 文档目录
```

---

## ⚙️ Configuration / 配置说明

### X/Twitter API Setup / X接口配置

1. Create a developer account at [developer.x.com](https://developer.x.com)
2. Create a project and get your Bearer Token
3. Add to `config.json`:

```json
{
  "sources": {
    "api": [
      {
        "name": "X-Twitter-AI",
        "type": "twitter",
        "bearer_token": "YOUR_BEARER_TOKEN",
        "query": "AI OR \"artificial intelligence\" OR GPT -is:retweet",
        "enabled": true
      }
    ]
  }
}
```

---

## 🛠️ Development Roadmap / 开发计划

- [x] Multi-source data collection / 多源数据采集
- [x] AI-powered analysis / AI智能分析
- [x] Keyword subscription / 关键词订阅
- [x] Web dashboard / Web管理界面
- [x] Chat interaction / 聊天交互
- [x] **X/Twitter integration** / **X/Twitter接入**
- [ ] Email notifications / 邮件推送
- [ ] Data visualization / 数据可视化
- [ ] Docker deployment / Docker部署

---

## 🤝 Contributing / 贡献

Contributions are welcome! Please feel free to submit a Pull Request.

欢迎提交 Issue 和 PR！

---

## 📄 License / 许可证

MIT License © 2025 StellarPulse Contributors
