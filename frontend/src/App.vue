<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, provide } from "vue";
import { APP_CODE, APP_NAME } from "./constants/app";
import { REQUEST_MESSAGES } from "./constants/messages";
import { routes } from "./routes";
import OverviewView from "./views/OverviewView.vue";
import BookingView from "./views/BookingView.vue";

const currentHash = ref(window.location.hash || "#/");
const refreshKey = ref(0);

function goHealth() {
  window.location.href = REQUEST_MESSAGES.healthPath;
}

function navigate(path: string) {
  window.location.hash = path;
  currentHash.value = path;
}

function handleHashChange() {
  const oldHash = currentHash.value.replace("#", "");
  const newHash = (window.location.hash || "#/").replace("#", "");
  currentHash.value = window.location.hash || "#/";
  if (oldHash === "/booking" && newHash === "/") {
    refreshKey.value++;
  }
}

function triggerRefresh() {
  refreshKey.value++;
}

provide("triggerRefresh", triggerRefresh);

const currentRoute = computed(() => {
  const hash = currentHash.value.replace("#", "");
  if (hash === "/booking") {
    return { path: "/booking", component: BookingView };
  }
  return { path: "/", component: OverviewView };
});

const activeNav = computed(() => {
  const hash = currentHash.value.replace("#", "");
  return hash === "/booking" ? "/booking" : "/";
});

onMounted(() => {
  window.addEventListener("hashchange", handleHashChange);
});

onUnmounted(() => {
  window.removeEventListener("hashchange", handleHashChange);
});
</script>

<template>
  <main class="app-shell">
    <header class="topbar">
      <div class="brand-wrap">
        <span class="brand-code">{{ APP_CODE }}</span>
        <h1 class="brand-title">{{ APP_NAME }}</h1>
      </div>
      <nav class="top-nav">
        <a
          v-for="route in routes"
          :key="route.path"
          class="nav-link"
          :class="{ active: activeNav === route.path }"
          @click.prevent="navigate(route.path)"
        >
          {{ route.label }}
        </a>
        <el-button type="primary" @click="navigate('/booking')">我要预约</el-button>
      </nav>
    </header>
    <component :is="currentRoute.component" :key="`${currentRoute.path}-${refreshKey}`" />
  </main>
</template>

<style scoped>
.brand-wrap {
  display: flex;
  flex-direction: column;
}

.top-nav {
  display: flex;
  align-items: center;
  gap: 24px;
}

.nav-link {
  color: color-mix(in srgb, #1d2229 70%, #546a7b 30%);
  text-decoration: none;
  font-weight: 600;
  padding: 6px 4px;
  border-bottom: 2px solid transparent;
  transition: all 0.2s ease;
  cursor: pointer;
}

.nav-link:hover {
  color: #546a7b;
}

.nav-link.active {
  color: #1d2229;
  border-bottom-color: #b84a37;
}

@media (max-width: 720px) {
  .topbar {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .top-nav {
    width: 100%;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
  }

  .nav-link {
    font-size: 14px;
  }
}
</style>
