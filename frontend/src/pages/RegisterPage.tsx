import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { Input } from "../components/common/Input";
import { Button } from "../components/common/Button";
import { UserPlus } from "lucide-react";

const registerSchema = z.object({
  username: z
    .string()
    .min(3, "Username must be at least 3 characters.")
    .max(50, "Username must not exceed 50 characters.")
    .regex(/^[a-zA-Z0-9_-]+$/, "Letters, numbers, underscores, and hyphens only."),
  email: z.string().email("Please enter a valid email address."),
  password: z.string().min(6, "Password must be at least 6 characters."),
});

type RegisterFormInput = z.infer<typeof registerSchema>;

export const RegisterPage: React.FC = () => {
  const { register: registerUser } = useAuth();
  const navigate = useNavigate();
  const [apiError, setApiError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterFormInput>({
    resolver: zodResolver(registerSchema),
  });

  const onSubmit = async (data: RegisterFormInput) => {
    try {
      setApiError(null);
      await registerUser(data);
      navigate("/dashboard");
    } catch (err: any) {
      const msg = err.response?.data?.message || "Registration failed. Please try again.";
      setApiError(msg);
    }
  };

  return (
    <div className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-xl space-y-6">
      <div className="text-center space-y-2">
        <div className="inline-flex p-3 bg-indigo-500/10 text-indigo-400 rounded-2xl mb-1">
          <UserPlus className="w-6 h-6" />
        </div>
        <h2 className="text-2xl font-bold text-slate-100">Create your account</h2>
        <p className="text-sm text-slate-400">Start building positive habits today</p>
      </div>

      {apiError && (
        <div className="p-3 bg-rose-500/10 border border-rose-500/20 text-rose-300 text-sm rounded-xl text-center">
          {apiError}
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <Input
          label="Username"
          type="text"
          placeholder="sarah_connor"
          error={errors.username?.message}
          {...register("username")}
        />

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
          Create Account
        </Button>
      </form>

      <p className="text-center text-xs text-slate-400">
        Already have an account?{" "}
        <Link to="/login" className="text-indigo-400 hover:underline font-medium">
          Log in
        </Link>
      </p>
    </div>
  );
};
