<script setup lang="ts">
import { onMounted, ref } from "vue";
import { fetchOverview, fetchTodayBookingCount } from "../api/client";
import { APP_CODE, APP_NAME } from "../constants/app";
import { REQUEST_MESSAGES } from "../constants/messages";
import { createFallbackOverview } from "../state/dashboard";
import type { OverviewResponse, TodayBookingCount } from "../types";
import FeatureStrip from "../components/FeatureStrip.vue";
import MetricGrid from "../components/MetricGrid.vue";
import OperationsTable from "../components/OperationsTable.vue";

const overview = ref<OverviewResponse>(createFallbackOverview());
const todayBookingCount = ref<TodayBookingCount>({ count: 0 });
const notice = ref(REQUEST_MESSAGES.overviewFallback);

function goHealth() {
  window.location.href = REQUEST_MESSAGES.healthPath;
}

function goBooking() {
  window.location.hash = "#/booking";
}

async function loadTodayBookingCount() {
  try {
    todayBookingCount.value = await fetchTodayBookingCount();
    const bookingKpi = overview.value.kpis.find((k) => k.label === "今日新增预约");
    if (bookingKpi) {
      bookingKpi.value = todayBookingCount.value.count.toString();
    } else {
      overview.value.kpis.splice(1, 0, {
        label: "今日新增预约",
        value: todayBookingCount.value.count.toString(),
        trend: "实时更新",
        tone: "warm",
      });
    }
  } catch {
    const bookingKpi = overview.value.kpis.find((k) => k.label === "今日新增预约");
    if (!bookingKpi) {
      overview.value.kpis.splice(1, 0, {
        label: "今日新增预约",
        value: "0",
        trend: "实时更新",
        tone: "warm",
      });
    }
  }
}

onMounted(async () => {
  try {
    overview.value = await fetchOverview();
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
