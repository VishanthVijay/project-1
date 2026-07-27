import { axiosClient } from "./axiosClient";
import type {
  ApiResponse,
  Habit,
  HabitCreateInput,
  HabitUpdateInput,
  HabitLog,
  HabitStats,
} from "../types";

export const habitApi = {
  getHabits: async (): Promise<Habit[]> => {
    const res = await axiosClient.get<ApiResponse<Habit[]>>("/habits");
    return res.data.data;
  },

  getHabitById: async (habitId: number): Promise<Habit> => {
    const res = await axiosClient.get<ApiResponse<Habit>>(`/habits/${habitId}`);
    return res.data.data;
  },

  createHabit: async (payload: HabitCreateInput): Promise<Habit> => {
    const res = await axiosClient.post<ApiResponse<Habit>>("/habits", payload);
    return res.data.data;
  },

  updateHabit: async (habitId: number, payload: HabitUpdateInput): Promise<Habit> => {
    const res = await axiosClient.put<ApiResponse<Habit>>(`/habits/${habitId}`, payload);
    return res.data.data;
  },

  deleteHabit: async (habitId: number): Promise<void> => {
    await axiosClient.delete<ApiResponse<{ deleted_habit_id: number }>>(`/habits/${habitId}`);
  },

  completeHabit: async (habitId: number, completed_date?: string): Promise<HabitLog> => {
    const res = await axiosClient.post<ApiResponse<HabitLog>>(`/habits/${habitId}/complete`, {
      completed_date,
    });
    return res.data.data;
  },

  removeCompletion: async (habitId: number, logId: number): Promise<void> => {
    await axiosClient.delete<ApiResponse<any>>(`/habits/${habitId}/complete/${logId}`);
  },

  getHabitHistory: async (habitId: number): Promise<HabitLog[]> => {
    const res = await axiosClient.get<ApiResponse<HabitLog[]>>(`/habits/${habitId}/history`);
    return res.data.data;
  },

  getHabitStats: async (habitId: number): Promise<HabitStats> => {
    const res = await axiosClient.get<ApiResponse<HabitStats>>(`/habits/${habitId}/stats`);
    return res.data.data;
  },
};
