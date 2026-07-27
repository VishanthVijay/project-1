import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { useAuth } from "../context/AuthContext";
import { habitApi } from "../api/habitApi";
import type { Habit, HabitCreateInput, HabitStats, HabitLog } from "../types";
import { HabitCard } from "../components/habits/HabitCard";
import { HabitFormModal } from "../components/habits/HabitFormModal";
import { ConfirmModal } from "../components/common/ConfirmModal";
import { EmptyState } from "../components/common/EmptyState";
import { Spinner } from "../components/common/Spinner";
import { Button } from "../components/common/Button";
import { ToastContainer } from "../components/common/Toast";
import type { ToastMessage } from "../components/common/Toast";
import { Plus, Flame, CheckCircle, Target } from "lucide-react";

export const DashboardPage: React.FC = () => {
  const { user } = useAuth();
  const queryClient = useQueryClient();

  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingHabit, setEditingHabit] = useState<Habit | null>(null);
  const [deletingHabitId, setDeletingHabitId] = useState<number | null>(null);
  const [toasts, setToasts] = useState<ToastMessage[]>([]);

  const addToast = (type: "success" | "error", message: string) => {
    const id = Math.random().toString(36).substring(2, 9);
    setToasts((prev) => [...prev, { id, type, message }]);
  };

  const removeToast = (id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  };

  // 1. Fetch User Habits Query
  const {
    data: habits = [],
    isLoading: isLoadingHabits,
    isError,
  } = useQuery({
    queryKey: ["habits"],
    queryFn: habitApi.getHabits,
  });

  // 2. Fetch Stats for Each Habit Query
  const statsQueries = useQuery({
    queryKey: ["habits", "stats", habits.map((h) => h.id)],
    queryFn: async () => {
      const statsMap: Record<number, HabitStats> = {};
      await Promise.all(
        habits.map(async (h) => {
          try {
            const stats = await habitApi.getHabitStats(h.id);
            statsMap[h.id] = stats;
          } catch (err) {
            console.error(`Failed to fetch stats for habit ${h.id}`, err);
          }
        })
      );
      return statsMap;
    },
    enabled: habits.length > 0,
  });

  // 3. Fetch Completion History Query
  const historiesQueries = useQuery({
    queryKey: ["habits", "history", habits.map((h) => h.id)],
    queryFn: async () => {
      const historiesMap: Record<number, HabitLog[]> = {};
      await Promise.all(
        habits.map(async (h) => {
          try {
            const logs = await habitApi.getHabitHistory(h.id);
            historiesMap[h.id] = logs;
          } catch (err) {
            console.error(`Failed to fetch history for habit ${h.id}`, err);
          }
        })
      );
      return historiesMap;
    },
    enabled: habits.length > 0,
  });

  const statsMap = statsQueries.data || {};
  const historiesMap = historiesQueries.data || {};

  const todayStr = new Date().toISOString().split("T")[0];
  const isCompletedToday = (habitId: number) => {
    const logs = historiesMap[habitId] || [];
    return logs.some((log) => log.completed_date === todayStr);
  };

  // Mutations with Toast Notifications
  const createMutation = useMutation({
    mutationFn: habitApi.createHabit,
    onSuccess: (newHabit) => {
      queryClient.invalidateQueries({ queryKey: ["habits"] });
      addToast("success", `Habit '${newHabit.title}' created successfully.`);
    },
    onError: (err: any) => {
      addToast("error", err.response?.data?.message || "Failed to create habit.");
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, input }: { id: number; input: HabitCreateInput }) =>
      habitApi.updateHabit(id, input),
    onSuccess: (updatedHabit) => {
      queryClient.invalidateQueries({ queryKey: ["habits"] });
      addToast("success", `Habit '${updatedHabit.title}' updated successfully.`);
    },
    onError: (err: any) => {
      addToast("error", err.response?.data?.message || "Failed to update habit.");
    },
  });

  const deleteMutation = useMutation({
    mutationFn: habitApi.deleteHabit,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["habits"] });
      setDeletingHabitId(null);
      addToast("success", "Habit deleted successfully.");
    },
    onError: (err: any) => {
      addToast("error", err.response?.data?.message || "Failed to delete habit.");
    },
  });

  const toggleCompleteMutation = useMutation({
    mutationFn: async (habitId: number) => {
      const logs = historiesMap[habitId] || [];
      const todayLog = logs.find((l) => l.completed_date === todayStr);
      if (todayLog) {
        await habitApi.removeCompletion(habitId, todayLog.id);
        return { action: "removed", habitId };
      } else {
        await habitApi.completeHabit(habitId, todayStr);
        return { action: "completed", habitId };
      }
    },
    onSuccess: (res) => {
      queryClient.invalidateQueries({ queryKey: ["habits"] });
      if (res.action === "completed") {
        addToast("success", "Habit marked complete for today!");
      } else {
        addToast("success", "Habit completion removed.");
      }
    },
    onError: (err: any) => {
      addToast("error", err.response?.data?.message || "Failed to update completion status.");
    },
  });

  const handleCreateOrUpdate = async (values: HabitCreateInput) => {
    if (editingHabit) {
      await updateMutation.mutateAsync({ id: editingHabit.id, input: values });
    } else {
      await createMutation.mutateAsync(values);
    }
  };

  const handleOpenCreate = () => {
    setEditingHabit(null);
    setIsFormOpen(true);
  };

  const handleOpenEdit = (habit: Habit) => {
    setEditingHabit(habit);
    setIsFormOpen(true);
  };

  const totalHabits = habits.length;
  const totalCompletions = Object.values(statsMap).reduce(
    (acc, curr) => acc + (curr?.total_completed_days || 0),
    0
  );
  const maxActiveStreak = Object.values(statsMap).reduce(
    (max, curr) => Math.max(max, curr?.current_streak || 0),
    0
  );

  return (
    <div className="space-y-8">
      {/* Header & Greeting */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-6 border-b border-slate-800">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-100 tracking-tight">
            Hello, {user?.username} 👋
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Track your daily progress, stay consistent, and hit your target streaks.
          </p>
        </div>
        <Button onClick={handleOpenCreate} variant="primary" size="md">
          <Plus className="w-4 h-4" />
          Add New Habit
        </Button>
      </div>

      {/* Overview Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl flex items-center space-x-4 shadow-md">
          <div className="p-3 bg-indigo-500/10 text-indigo-400 rounded-xl">
            <Target className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs font-medium text-slate-400">Total Habits</p>
            <p className="text-2xl font-bold text-slate-100">{totalHabits}</p>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl flex items-center space-x-4 shadow-md">
          <div className="p-3 bg-amber-500/10 text-amber-400 rounded-xl">
            <Flame className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs font-medium text-slate-400">Top Active Streak</p>
            <p className="text-2xl font-bold text-slate-100">{maxActiveStreak} days</p>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-5 rounded-2xl flex items-center space-x-4 shadow-md">
          <div className="p-3 bg-emerald-500/10 text-emerald-400 rounded-xl">
            <CheckCircle className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs font-medium text-slate-400">Total Completions</p>
            <p className="text-2xl font-bold text-slate-100">{totalCompletions}</p>
          </div>
        </div>
      </div>

      {/* Main Habits List */}
      {isLoadingHabits ? (
        <div className="py-12">
          <Spinner size="lg" />
        </div>
      ) : isError ? (
        <div className="p-6 bg-rose-500/10 border border-rose-500/20 text-rose-300 rounded-2xl text-center">
          Failed to load habits. Please ensure your backend server is running.
        </div>
      ) : habits.length === 0 ? (
        <EmptyState
          title="No habits created yet"
          description="Build consistency by creating your first daily habit today."
          actionLabel="Create Habit"
          onAction={handleOpenCreate}
        />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {habits.map((habit) => (
            <HabitCard
              key={habit.id}
              habit={habit}
              stats={statsMap[habit.id]}
              isCompletedToday={isCompletedToday(habit.id)}
              onToggleComplete={(id) => toggleCompleteMutation.mutate(id)}
              onEdit={handleOpenEdit}
              onDelete={(id) => setDeletingHabitId(id)}
            />
          ))}
        </div>
      )}

      {/* Form Modal */}
      <HabitFormModal
        isOpen={isFormOpen}
        onClose={() => setIsFormOpen(false)}
        onSubmit={handleCreateOrUpdate}
        initialData={editingHabit}
      />

      {/* Confirmation Modal */}
      <ConfirmModal
        isOpen={deletingHabitId !== null}
        onClose={() => setDeletingHabitId(null)}
        onConfirm={() => deletingHabitId && deleteMutation.mutate(deletingHabitId)}
        title="Delete Habit"
        message="Are you sure you want to delete this habit? All associated daily completion history will be permanently deleted."
        isLoading={deleteMutation.isPending}
      />

      {/* Toast Notification Overlay */}
      <ToastContainer toasts={toasts} onDismiss={removeToast} />
    </div>
  );
};
