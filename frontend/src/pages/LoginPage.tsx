import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { authApi } from "../api/authApi";
import { Input } from "../components/common/Input";
import { Button } from "../components/common/Button";
import { LogIn } from "lucide-react";

const loginSchema = z.object({
  email: z.string().email("Please enter a valid email address."),
  password: z.string().min(1, "Password is required."),
});

type LoginFormInput = z.infer<typeof loginSchema>;

export const LoginPage: React.FC = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [apiError, setApiError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormInput>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormInput) => {
    try {
      setApiError(null);
      const tokenRes = await authApi.login(data);
      await login(tokenRes.access_token);
      navigate("/dashboard");
    } catch (err: any) {
      const msg = err.response?.data?.message || "Invalid email or password. Please try again.";
      setApiError(msg);
    }
  };

  return (
    <div className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-xl space-y-6">
      <div className="text-center space-y-2">
        <div className="inline-flex p-3 bg-indigo-500/10 text-indigo-400 rounded-2xl mb-1">
          <LogIn className="w-6 h-6" />
        </div>
        <h2 className="text-2xl font-bold text-slate-100">Welcome back</h2>
        <p className="text-sm text-slate-400">Log in to track your habits and maintain your streak</p>
      </div>

      {apiError && (
        <div className="p-3 bg-rose-500/10 border border-rose-500/20 text-rose-300 text-sm rounded-xl text-center">
          {apiError}
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <Input
          label="Email Address"
          type="email"
          placeholder="sarah@example.com"
          error={errors.email?.message}
          {...register("email")}
        />

        <Input
          label="Password"
          type="password"
          placeholder="••••••••"
          error={errors.password?.message}
          {...register("password")}
        />

        <Button type="submit" variant="primary" className="w-full" isLoading={isSubmitting}>
          Log In
        </Button>
      </form>

      <p className="text-center text-xs text-slate-400">
        Don't have an account?{" "}
        <Link to="/register" className="text-indigo-400 hover:underline font-medium">
          Create account
        </Link>
      </p>
    </div>
  );
};
