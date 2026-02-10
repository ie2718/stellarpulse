#!/usr/bin/env python3
"""
StellarPulse Chat Bot - 消息交互入口
集成到主监控系统中
"""

import sys
import json
sys.path.insert(0, '/home/ec2-user/stellarpulse')

from chat_handler import handle_command, handle_number, should_respond

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 chat_bot.py '<message>'")
        sys.exit(1)
    
    message = sys.argv[1]
    
    # 检查是否应该响应
    if not should_respond(message):
        print("SKIP")
        sys.exit(0)
    
    # 处理数字回复 (查看详情)
    if message.strip().isdigit():
        result = handle_number(message.strip())
        if result:
            print(result)
        else:
            print("❌ 无效的选择，请重试")
        sys.exit(0)
    
    # 处理命令
    result = handle_command(message)
    print(result)

if __name__ == '__main__':
    main()
