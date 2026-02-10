#!/bin/bash
# StellarPulse 消息处理器
# 用于集成到 OpenClaw 自动响应

MESSAGE="$1"

if [ -z "$MESSAGE" ]; then
    exit 0
fi

# 运行 chat_bot.py 并捕获输出
OUTPUT=$(cd /home/ec2-user/stellarpulse && python3 chat_bot.py "$MESSAGE" 2>&1)

# 如果输出不是 SKIP，则返回
if [ "$OUTPUT" != "SKIP" ]; then
    echo "$OUTPUT"
fi
