export interface ApiResponse<T> {
  success: boolean;
  message: string;
  data: T;
  errors?: any;
}

export interface User {
  id: number;
  username: string;
  email: string;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface Habit {
  id: number;
  title: string;
  description?: string;
  category: string;
  frequency: string;
  created_at: string;
}

export interface HabitCreateInput {
  title: string;
  description?: string;
  category: string;
  frequency: string;
}

export interface HabitUpdateInput {
  title?: string;
  description?: string;
  category?: string;
  frequency?: string;
}

export interface HabitLog {
  id: number;
  habit_id: number;
  completed_date: string;
  completed: boolean;
}

export interface HabitStats {
  habit_id: number;
  current_streak: number;
  longest_streak: number;
  total_completed_days: number;
  last_completed_date?: string;
}
