# 架构

```
client/proxy_skeleton.py ──▶ server/app.py ──▶ server/scheduler.py
                                   │
                        server/accounts.py · server/security.py
```

客户端只截一次报文；后端持有凭据并负责执行、重试、通知。轨迹与平台适配不在本仓库。
