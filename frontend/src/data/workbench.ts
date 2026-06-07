import type { FeatureItem, KpiItem, OperationRecord } from "../types";

export const localFeatures: FeatureItem[] = [
  {
    "id": 1,
    "title": "场地与场次管理",
    "description": "配置野战场地信息（丛林/废墟/城市巷战），设置每日开放场次（上午场/下午场/夜场），每场限制人数上限，支持特殊天气闭场。",
    "status": "已上线",
    "metric": "88%"
  },
  {
    "id": 2,
    "title": "战队组建与约战",
    "description": "玩家创建或加入战队，战队队长可发起约战挑战，选择对手战队、场地和场次，对方确认后生成对战订单。",
    "status": "排期中",
    "metric": "31 单"
  },
  {
    "id": 3,
    "title": "装备租赁管理",
    "description": "管理可租赁装备（仿真枪/护甲/护目镜/迷彩服），记录装备状态（完好/维修中/报废），玩家预约时可选择租赁装备套餐。",
    "status": "巡检中",
    "metric": "10 项"
  },
  {
    "id": 4,
    "title": "战绩统计与赛季排行榜",
    "description": "记录每局对战的击杀数、死亡数、生存时长、胜率等数据，生成个人和战队赛季排行榜，颁发段位勋章。",
    "status": "优化中",
    "metric": "4 级"
  },
  {
    "id": 5,
    "title": "套餐组合（团建/亲子）",
    "description": "预设多种套餐（团建套餐含教练/裁判/摄影，亲子套餐降低对抗强度），企业客户可预约团建包场，一次性安排多场次。",
    "status": "可导出",
    "metric": "28 条"
  }
];

export const localKpis: KpiItem[] = [
  {
    "label": "今日处理",
    "value": "110",
    "trend": "+12%",
    "tone": "primary"
  },
  {
    "label": "预约/订单",
    "value": "49",
    "trend": "+8%",
    "tone": "warm"
  },
  {
    "label": "履约率",
    "value": "89%",
    "trend": "+3%",
    "tone": "cool"
  },
  {
    "label": "待处理",
    "value": "6",
    "trend": "需跟进",
    "tone": "neutral"
  }
];

export const operationRecords: OperationRecord[] = [
  {
    "key": "ldairsoftcs-1",
    "name": "场地与场次管理",
    "owner": "运营组",
    "status": "已上线",
    "metric": "88%",
    "priority": "高"
  },
  {
    "key": "ldairsoftcs-2",
    "name": "战队组建与约战",
    "owner": "管理员",
    "status": "排期中",
    "metric": "31 单",
    "priority": "中"
  },
  {
    "key": "ldairsoftcs-3",
    "name": "装备租赁管理",
    "owner": "服务台",
    "status": "巡检中",
    "metric": "10 项",
    "priority": "低"
  },
  {
    "key": "ldairsoftcs-4",
    "name": "战绩统计与赛季排行榜",
    "owner": "财务组",
    "status": "优化中",
    "metric": "4 级",
    "priority": "高"
  },
  {
    "key": "ldairsoftcs-5",
    "name": "套餐组合（团建/亲子）",
    "owner": "审核组",
    "status": "可导出",
    "metric": "28 条",
    "priority": "中"
  }
];
