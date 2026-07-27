import { axiosClient } from "./axiosClient";
import type { ApiResponse, User, TokenResponse } from "../types";

export const authApi = {
  register: async (payload: { username: string; email: string; password: string }): Promise<User> => {
    const res = await axiosClient.post<ApiResponse<User>>("/auth/register", payload);
    return res.data.data;
  },

  login: async (payload: { email: string; password: string }): Promise<TokenResponse> => {
    const res = await axiosClient.post<ApiResponse<TokenResponse>>("/auth/login", payload);
    return res.data.data;
  },

  getMe: async (): Promise<User> => {
    const res = await axiosClient.get<ApiResponse<User>>("/auth/me");
    return res.data.data;
  },
};
