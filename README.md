# 真人CS野战预约系统

面向真人CS/野战拓展基地，提供场地预约、战队对战和装备租赁管理的综合平台。

## Docker Compose 快速启动

首次启动前复制环境变量文件：

```bash
cp .env.example .env
docker compose up -d
```

访问地址：

- 前端：http://localhost:28508
- 后端健康检查：http://localhost:29508/health
- API 示例：http://localhost:28508/api/overview

## 项目主要功能

- 场地与场次管理：配置野战场地信息（丛林/废墟/城市巷战），设置每日开放场次（上午场/下午场/夜场），每场限制人数上限，支持特殊天气闭场。
- 战队组建与约战：玩家创建或加入战队，战队队长可发起约战挑战，选择对手战队、场地和场次，对方确认后生成对战订单。
- 装备租赁管理：管理可租赁装备（仿真枪/护甲/护目镜/迷彩服），记录装备状态（完好/维修中/报废），玩家预约时可选择租赁装备套餐。
- 战绩统计与赛季排行榜：记录每局对战的击杀数、死亡数、生存时长、胜率等数据，生成个人和战队赛季排行榜，颁发段位勋章。
- 套餐组合（团建/亲子）：预设多种套餐（团建套餐含教练/裁判/摄影，亲子套餐降低对抗强度），企业客户可预约团建包场，一次性安排多场次。

## 本地开发方式

前端：

```bash
cd frontend
npm install
npm run dev
```

后端：

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 29508
```

## 技术栈

| 分层 | 技术 |
| --- | --- |
| 前端 | Vue 3 + TypeScript、Element Plus、Vite |
| 后端 | FastAPI + Python |
| 数据库 | PostgreSQL |
| 认证 | JWT |
| 依赖 | SQLAlchemy、Pydantic |

## 项目目录结构

```text
.
├── backend/              # 后端服务
├── database/             # 数据库脚本
├── frontend/             # 前端应用
├── docker-compose.yml    # 一键部署编排
├── .env.example          # 环境变量示例
└── README.md
```

## 环境变量说明

| 变量 | 说明 | 默认值 |
| --- | --- | --- |
| COMPOSE_PROJECT_NAME | Compose 项目名，避免中文目录名导致项目名为空 | ldairsoftcs |
| DB_NAME | 数据库名称 | app |
| DB_USER | 数据库用户 | app |
| DB_PASSWORD | 数据库密码 | app_pwd |
| DB_ROOT_PASSWORD | 数据库 root 密码 | root_pwd |
| JWT_SECRET | JWT 签名密钥 | change_me_to_a_long_random_string |
| FRONTEND_PORT | 前端宿主机端口 | 28508 |
| BACKEND_PORT | 后端宿主机端口 | 29508 |
| DB_PORT | 数据库宿主机端口 | 5432 |

## Docker 部署说明

- 使用 `docker compose up -d` 启动，不需要额外传入 `-p`。
- `docker-compose.yml` 顶层已声明 `name: ldairsoftcs`，并且 `.env` 包含 `COMPOSE_PROJECT_NAME=ldairsoftcs`，可在中文目录名下启动。
- 数据库数据保存在命名卷 `db_data` 中，不依赖当前目录名。
- 前端容器由 Nginx 托管静态资源，并把 `/api/` 反向代理到 `backend:29508`。
- 若本地端口冲突，可修改 `.env` 中的 `FRONTEND_PORT`、`BACKEND_PORT`、`DB_PORT`。

常用命令：

```bash
docker compose config --quiet
docker compose ps
docker compose down
```

## License

MIT
