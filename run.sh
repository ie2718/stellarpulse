#!/bin/bash
# 运行监控并发送WhatsApp通知

cd /home/ec2-user/tech-monitor

# 运行Python脚本并捕获输出
OUTPUT=$(python3 monitor.py 2>&1)

# 提取WhatsApp消息
MSG=$(echo "$OUTPUT" | sed -n '/WHATSAPP_MSG_START/,/WHATSAPP_MSG_END/p' | sed '1d;$d')

# 如果有消息，发送WhatsApp
if [ -n "$MSG" ]; then
    # 使用OpenClaw的消息工具发送
    echo "$MSG" > /tmp/tech_monitor_msg.txt
fi

# 输出日志
echo "$OUTPUT"
