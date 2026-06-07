import { localFeatures, localKpis, operationRecords } from "../data/workbench";
import type { OverviewResponse } from "../types";
import { APP_CODE, APP_NAME } from "../constants/app";

export function createFallbackOverview(): OverviewResponse {
  return {
    appName: APP_NAME,
    appCode: APP_CODE,
    description: "面向真人CS/野战拓展基地，提供场地预约、战队对战和装备租赁管理的综合平台。",
    features: localFeatures,
    kpis: localKpis,
    records: operationRecords,
  };
}
