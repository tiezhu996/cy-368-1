<script setup lang="ts">
import { ref, computed, watch, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import {
  fetchFields,
  fetchAvailableSlots,
  submitBooking,
} from "../api/client";
import type { Field, AvailableSlot, BookingRequest } from "../types";
import { APP_CODE, APP_NAME } from "../constants/app";

const fields = ref<Field[]>([]);
const availableSlots = ref<AvailableSlot[]>([]);
const loading = ref(false);
const submitting = ref(false);

const form = ref({
  player_name: "",
  phone: "",
  booking_date: "",
  field_id: null as number | null,
  slot_id: null as number | null,
  player_count: 1,
  remark: "",
});

const today = computed(() => {
  const d = new Date();
  return d.toISOString().split("T")[0];
});

const maxDate = computed(() => {
  const d = new Date();
  d.setMonth(d.getMonth() + 1);
  return d.toISOString().split("T")[0];
});

const selectedField = computed(() => {
  return fields.value.find((f) => f.id === form.value.field_id);
});

const selectedSlot = computed(() => {
  return availableSlots.value.find((s) => s.id === form.value.slot_id);
});

const isFormValid = computed(() => {
  return (
    form.value.player_name.trim() &&
    form.value.phone.trim() &&
    form.value.booking_date &&
    form.value.field_id !== null &&
    form.value.slot_id !== null &&
    form.value.player_count >= 1 &&
    form.value.player_count <= 30
  );
});

function goOverview() {
  window.location.hash = "";
  window.location.href = "/";
}

async function loadFields() {
  try {
    loading.value = true;
    fields.value = await fetchFields();
    if (fields.value.length > 0 && form.value.field_id === null) {
      form.value.field_id = fields.value[0].id;
    }
  } catch (error) {
    ElMessage.error("加载场地信息失败");
  } finally {
    loading.value = false;
  }
}

async function loadAvailableSlots() {
  if (!form.value.booking_date || form.value.field_id === null) {
    availableSlots.value = [];
    return;
  }

  try {
    loading.value = true;
    availableSlots.value = await fetchAvailableSlots(
      form.value.booking_date,
      form.value.field_id
    );
    const activeSlot = availableSlots.value.find((s) => !s.is_full);
    if (activeSlot && form.value.slot_id === null) {
      form.value.slot_id = activeSlot.id;
    }
  } catch (error) {
    ElMessage.error("加载场次信息失败");
  } finally {
    loading.value = false;
  }
}

function formatTime(timeStr: string) {
  return timeStr.substring(0, 5);
}

function getSlotStatusText(slot: AvailableSlot) {
  if (slot.is_full) return "已满";
  if (slot.remaining_count <= 5) return `仅剩${slot.remaining_count}位`;
  return `${slot.remaining_count}位可约`;
}

function getSlotStatusClass(slot: AvailableSlot) {
  if (slot.is_full) return "slot-full";
  if (slot.remaining_count <= 5) return "slot-urgent";
  return "slot-available";
}

watch(
  () => [form.value.booking_date, form.value.field_id],
  () => {
    form.value.slot_id = null;
    loadAvailableSlots();
  }
);

async function handleSubmit() {
  if (!isFormValid.value) {
    ElMessage.warning("请完整填写预约信息");
    return;
  }

  if (selectedSlot.value?.is_full) {
    ElMessage.warning("该场次已满，请选择其他场次");
    return;
  }

  if (
    selectedSlot.value &&
    form.value.player_count > selectedSlot.value.remaining_count
  ) {
    ElMessage.warning(
      `预约人数超过剩余名额，当前剩余 ${selectedSlot.value.remaining_count} 人`
    );
    return;
  }

  try {
    const confirmText = `确认预约：\n场地：${selectedField.value?.name}\n日期：${form.value.booking_date}\n场次：${selectedSlot.value?.name}\n人数：${form.value.player_count}人`;
    await ElMessageBox.confirm(confirmText, "预约确认", {
      confirmButtonText: "确认预约",
      cancelButtonText: "再想想",
      type: "info",
    });
  } catch {
    return;
  }

  try {
    submitting.value = true;
    const bookingData: BookingRequest = {
      player_name: form.value.player_name.trim(),
      phone: form.value.phone.trim(),
      booking_date: form.value.booking_date,
      field_id: form.value.field_id!,
      slot_id: form.value.slot_id!,
      player_count: form.value.player_count,
      remark: form.value.remark.trim() || undefined,
    };
    const result = await submitBooking(bookingData);
    await ElMessageBox.alert(
      `预约成功！\n\n预约编号：${result.id}\n场地：${result.field_name}\n日期：${result.booking_date}\n场次：${result.slot_name}\n人数：${result.player_count}人`,
      "预约成功",
      {
        confirmButtonText: "好的",
        type: "success",
      }
    );
    form.value = {
      player_name: "",
      phone: "",
      booking_date: "",
      field_id: fields.value[0]?.id || null,
      slot_id: null,
      player_count: 1,
      remark: "",
    };
    window.location.href = "/";
  } catch (error: any) {
    ElMessage.error(error.message || "预约失败，请稍后重试");
  } finally {
    submitting.value = false;
  }
}

onMounted(() => {
  loadFields();
});
</script>

<template>
  <main class="app-shell">
    <header class="topbar">
      <div>
        <span class="brand-code">{{ APP_CODE }}</span>
        <h1 class="brand-title">{{ APP_NAME }}</h1>
      </div>
      <el-button type="primary" @click="goOverview">返回总览</el-button>
    </header>

    <section class="workspace">
      <div class="lead-grid">
        <article class="hero-panel">
          <span class="pill">在线预约</span>
          <h2>场地预约</h2>
          <p>选择您心仪的场地和场次，开启精彩的野战体验。支持预约未来30天内的场次。</p>
        </article>
      </div>

      <section class="work-panel booking-panel">
        <div v-loading="loading" class="booking-form">
          <div class="form-section">
            <h3>选择场地</h3>
            <div class="field-options">
              <div
                v-for="field in fields"
                :key="field.id"
                class="field-card"
                :class="{ active: form.field_id === field.id }"
                @click="form.field_id = field.id"
              >
                <div class="field-name">{{ field.name }}</div>
                <div class="field-desc">{{ field.description }}</div>
                <div class="field-meta">最多{{ field.max_players }}人</div>
              </div>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>选择日期</label>
              <el-date-picker
                v-model="form.booking_date"
                type="date"
                :min-date="today"
                :max-date="maxDate"
                placeholder="选择预约日期"
                value-format="YYYY-MM-DD"
                class="full-width"
                size="large"
              />
            </div>
            <div class="form-group">
              <label>预约人数</label>
              <el-input-number
                v-model="form.player_count"
                :min="1"
                :max="30"
                class="full-width"
                size="large"
              />
            </div>
          </div>

          <div class="form-section">
            <h3>选择场次</h3>
            <div v-if="availableSlots.length === 0" class="empty-slots">
              <p>请先选择场地和日期查看可用场次</p>
            </div>
            <div v-else class="slot-options">
              <div
                v-for="slot in availableSlots"
                :key="slot.id"
                class="slot-card"
                :class="{
                  active: form.slot_id === slot.id,
                  disabled: slot.is_full,
                }"
                @click="!slot.is_full && (form.slot_id = slot.id)"
              >
                <div class="slot-name">{{ slot.name }}</div>
                <div class="slot-time">
                  {{ formatTime(slot.start_time) }} -
                  {{ formatTime(slot.end_time) }}
                </div>
                <div class="slot-status" :class="getSlotStatusClass(slot)">
                  {{ getSlotStatusText(slot) }}
                </div>
              </div>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>玩家姓名</label>
              <el-input
                v-model="form.player_name"
                placeholder="请输入您的姓名"
                maxlength="80"
                size="large"
              />
            </div>
            <div class="form-group">
              <label>联系电话</label>
              <el-input
                v-model="form.phone"
                placeholder="请输入联系电话"
                maxlength="20"
                size="large"
              />
            </div>
          </div>

          <div class="form-group">
            <label>备注信息（选填）</label>
            <el-input
              v-model="form.remark"
              type="textarea"
              :rows="3"
              placeholder="如有特殊需求请备注，如装备租赁、战队预约等"
              maxlength="255"
            />
          </div>

          <div class="form-actions">
            <el-button size="large" @click="goOverview">取消</el-button>
            <el-button
              type="primary"
              size="large"
              :disabled="!isFormValid || submitting"
              :loading="submitting"
              @click="handleSubmit"
            >
              提交预约
            </el-button>
          </div>
        </div>
      </section>
    </section>
  </main>
</template>

<style scoped>
.booking-panel {
  margin-top: 26px;
}

.booking-form {
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.form-section h3 {
  margin: 0 0 14px;
  font-size: 18px;
  font-weight: 700;
  color: #1d2229;
}

.field-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 14px;
}

.field-card {
  padding: 18px;
  border: 1px solid color-mix(in srgb, #1d2229 13%, transparent);
  border-radius: 8px;
  background: color-mix(in srgb, #f5f6f1 86%, white 14%);
  cursor: pointer;
  transition: all 0.2s ease;
}

.field-card:hover {
  border-color: #546a7b;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px color-mix(in srgb, #1d2229 12%, transparent);
}

.field-card.active {
  border-color: #546a7b;
  background: color-mix(in srgb, #546a7b 8%, #f5f6f1);
  box-shadow: 0 4px 12px color-mix(in srgb, #546a7b 20%, transparent);
}

.field-name {
  font-weight: 700;
  font-size: 16px;
  margin-bottom: 6px;
}

.field-desc {
  font-size: 14px;
  color: color-mix(in srgb, #1d2229 70%, #546a7b 30%);
  line-height: 1.5;
  margin-bottom: 8px;
}

.field-meta {
  font-size: 13px;
  color: #546a7b;
  font-weight: 600;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 600;
  font-size: 14px;
  color: #1d2229;
}

.full-width {
  width: 100%;
}

.empty-slots {
  padding: 40px;
  text-align: center;
  background: color-mix(in srgb, #546a7b 6%, transparent);
  border-radius: 8px;
  color: color-mix(in srgb, #1d2229 60%, #546a7b 40%);
}

.slot-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 14px;
}

.slot-card {
  padding: 16px;
  border: 1px solid color-mix(in srgb, #1d2229 13%, transparent);
  border-radius: 8px;
  background: color-mix(in srgb, #f5f6f1 86%, white 14%);
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.slot-card:hover:not(.disabled) {
  border-color: #546a7b;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px color-mix(in srgb, #1d2229 12%, transparent);
}

.slot-card.active {
  border-color: #546a7b;
  background: color-mix(in srgb, #546a7b 8%, #f5f6f1);
  box-shadow: 0 4px 12px color-mix(in srgb, #546a7b 20%, transparent);
}

.slot-card.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: color-mix(in srgb, #1d2229 4%, #f5f6f1);
}

.slot-name {
  font-weight: 700;
  font-size: 15px;
  margin-bottom: 4px;
}

.slot-time {
  font-size: 13px;
  color: color-mix(in srgb, #1d2229 65%, #546a7b 35%);
  margin-bottom: 8px;
}

.slot-status {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
}

.slot-available {
  background: color-mix(in srgb, #546a7b 12%, transparent);
  color: #546a7b;
}

.slot-urgent {
  background: color-mix(in srgb, #b84a37 15%, transparent);
  color: #b84a37;
}

.slot-full {
  background: color-mix(in srgb, #1d2229 12%, transparent);
  color: color-mix(in srgb, #1d2229 60%, transparent);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 8px;
  border-top: 1px solid color-mix(in srgb, #1d2229 10%, transparent);
}

@media (max-width: 640px) {
  .form-row {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .form-actions {
    flex-direction: column-reverse;
  }

  .form-actions .el-button {
    width: 100%;
  }
}
</style>
