import { API_BASE_URL } from "../constants/app";
import type {
  OverviewResponse,
  Field,
  TimeSlot,
  AvailableSlot,
  BookingRequest,
  BookingResponse,
  TodayBookingCount,
} from "../types";

export async function fetchOverview(): Promise<OverviewResponse> {
  const response = await fetch(`${API_BASE_URL}/overview`, {
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    throw new Error(`Overview request failed: ${response.status}`);
  }

  return response.json() as Promise<OverviewResponse>;
}

export async function fetchFields(): Promise<Field[]> {
  const response = await fetch(`${API_BASE_URL}/api/fields`, {
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    throw new Error(`Fields request failed: ${response.status}`);
  }

  return response.json() as Promise<Field[]>;
}

export async function fetchTimeSlots(): Promise<TimeSlot[]> {
  const response = await fetch(`${API_BASE_URL}/api/time-slots`, {
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    throw new Error(`Time slots request failed: ${response.status}`);
  }

  return response.json() as Promise<TimeSlot[]>;
}

export async function fetchAvailableSlots(
  bookingDate: string,
  fieldId: number
): Promise<AvailableSlot[]> {
  const response = await fetch(
    `${API_BASE_URL}/api/available-slots?booking_date=${bookingDate}&field_id=${fieldId}`,
    {
      headers: { Accept: "application/json" },
    }
  );

  if (!response.ok) {
    throw new Error(`Available slots request failed: ${response.status}`);
  }

  return response.json() as Promise<AvailableSlot[]>;
}

export async function submitBooking(
  data: BookingRequest
): Promise<BookingResponse> {
  const response = await fetch(`${API_BASE_URL}/api/bookings`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: "预约失败" }));
    throw new Error(errorData.detail || `Booking request failed: ${response.status}`);
  }

  return response.json() as Promise<BookingResponse>;
}

export async function fetchTodayBookingCount(): Promise<TodayBookingCount> {
  const response = await fetch(`${API_BASE_URL}/api/bookings/today/count`, {
    headers: { Accept: "application/json" },
  });

  if (!response.ok) {
    throw new Error(`Today booking count request failed: ${response.status}`);
  }

  return response.json() as Promise<TodayBookingCount>;
}
