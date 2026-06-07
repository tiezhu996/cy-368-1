<script setup lang="ts">
import { onMounted, ref, computed } from "vue";
import { fetchOverview, fetchTodayBookingCount } from "../api/client";
import { APP_CODE, APP_NAME } from "../constants/app";
import { REQUEST_MESSAGES } from "../constants/messages";
import { createFallbackOverview } from "../state/dashboard";
import type { OverviewResponse, TodayBookingCount, KpiItem } from "../types";
import FeatureStrip from "../components/FeatureStrip.vue";
import MetricGrid from "../components/MetricGrid.vue";
import OperationsTable from "../components/OperationsTable.vue";

const baseOverview = ref<OverviewResponse>(createFallbackOverview());
const todayBookingCount = ref<TodayBookingCount>({ count: 0 });
const notice = ref(REQUEST_MESSAGES.overviewFallback);

const bookingKpi = computed<KpiItem>(() => ({
  label: "今日新增预约",
  value: todayBookingCount.value.count.toString(),
  trend: "实时更新",
  tone: "warm",
}));

const displayKpis = computed<KpiItem[]>(() => {
  const kpis = [...baseOverview.value.kpis];
  const existingIndex = kpis.findIndex((k) => k.label === "今日新增预约");
  if (existingIndex >= 0) {
    kpis[existingIndex] = bookingKpi.value;
  } else {
    kpis.splice(1, 0, bookingKpi.value);
  }
  return kpis;
});

const overview = computed<OverviewResponse>(() => ({
  ...baseOverview.value,
  kpis: displayKpis.value,
}));

function goHealth() {
  window.location.href = REQUEST_MESSAGES.healthPath;
}

function goBooking() {
  window.location.hash = "#/booking";
}

async function loadTodayBookingCount() {
  try {
    todayBookingCount.value = await fetchTodayBookingCount();
  } catch {
    todayBookingCount.value = { count: 0 };
  }
}

onMounted(async () => {
  try {
    baseOverview.value = await fetchOverview();
    notice.value = "后端服务已联通，当前展示实时接口数据。";
  } catch {
    notice.value = REQUEST_MESSAGES.overviewFallback;
  }
  loadTodayBookingCount();

  const interval = setInterval(loadTodayBookingCount, 30000);

  return () => clearInterval(interval);
});
</script>

<template>
  <div>
    <section class="workspace">
      <div class="lead-grid">
        <article class="hero-panel">
          <span class="pill">{{ notice }}</span>
          <h2>{{ overview.appName }}</h2>
          <p>{{ overview.description }}</p>
        </article>
        <MetricGrid :items="overview.kpis" />
      </div>
      <FeatureStrip :items="overview.features" />
      <section class="work-panel">
        <div class="panel-header">
          <h2>运营任务流</h2>
          <el-button type="primary" @click="goBooking">立即预约场地</el-button>
        </div>
        <OperationsTable :records="overview.records" />
      </section>
    </section>
  </div>
</template>

<style scoped>
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
}

.panel-header h2 {
  margin: 0;
}
</style>
