# TechMonitor 扩展计划

## 任务清单
- [ ] 1. 扩展数据源 (36氪, Reddit, arXiv, 更多RSS)
- [ ] 2. AI自动摘要 (提取关键信息)
- [ ] 3. 关键词订阅系统 (自定义关注词)
- [ ] 4. Web管理界面 (历史查看/配置/统计)
- [ ] 5. 整合测试

## 文件结构
```
~/tech-monitor/
├── monitor.py          # 主程序
├── config.json         # 配置文件
├── data.json           # 数据存储
├── keywords.json       # 用户关键词订阅
├── web/                # Web界面
│   ├── server.py
│   ├── templates/
│   └── static/
├── sources/            # 数据源模块
│   ├── __init__.py
│   ├── rss.py
│   ├── reddit.py
│   ├── hackernews.py
│   └── arxiv.py
└── reports/            # 报告输出
```
