# StellarPulse Configuration

## 配置文件说明

### config.json

主要配置文件，包含数据源、关键词、系统设置。

### keywords.json

用户关键词订阅数据，自动维护，无需手动编辑。

### data.json

采集的资讯数据缓存，自动维护。

## 环境变量

```bash
# 可选：自定义数据目录
export TECHMONITOR_DATA_DIR=/path/to/data

# 可选：开启调试模式
export TECHMONITOR_DEBUG=1
```
