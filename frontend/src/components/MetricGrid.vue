<script setup lang="ts">
import type { KpiItem } from "../types";

defineProps<{ items: KpiItem[] }>();
</script>

<template>
  <section class="metric-grid" aria-label="关键指标">
    <article
      v-for="item in items"
      :key="item.label"
      class="metric-card"
      :class="`tone-${item.tone}`"
    >
      <span>{{ item.label }}</span>
      <strong class="metric-value">{{ item.value }}</strong>
      <small>{{ item.trend }}</small>
    </article>
  </section>
</template>

<style scoped>
.tone-primary .metric-value {
  color: #546a7b;
}

.tone-warm .metric-value {
  color: #b84a37;
}

.tone-cool .metric-value {
  color: #2e6e7e;
}

.tone-neutral .metric-value {
  color: #6b7280;
}
</style>
