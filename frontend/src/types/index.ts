export interface FeatureItem {
  id: number;
  title: string;
  description: string;
  status: string;
  metric: string;
}

export interface KpiItem {
  label: string;
  value: string;
  trend: string;
  tone: string;
}

export interface OperationRecord {
  key: string;
  name: string;
  owner: string;
  status: string;
  metric: string;
  priority: string;
}

export interface OverviewResponse {
  appName: string;
  appCode: string;
  description: string;
  features: FeatureItem[];
  kpis: KpiItem[];
  records: OperationRecord[];
}

export interface Field {
  id: number;
  name: string;
  description: string;
  max_players: number;
}

export interface TimeSlot {
  id: number;
  name: string;
  start_time: string;
  end_time: string;
}

export interface AvailableSlot {
  id: number;
  name: string;
  start_time: string;
  end_time: string;
  max_players: number;
  booked_count: number;
  remaining_count: number;
  is_full: boolean;
}

export interface BookingRequest {
  player_name: string;
  phone: string;
  booking_date: string;
  field_id: number;
  slot_id: number;
  player_count: number;
  remark?: string;
}

export interface BookingResponse {
  id: number;
  player_name: string;
  phone: string;
  booking_date: string;
  field_id: number;
  field_name: string;
  slot_id: number;
  slot_name: string;
  player_count: number;
  status: string;
  remark: string;
  created_at: string | null;
}

export interface TodayBookingCount {
  count: number;
}
