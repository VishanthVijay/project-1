import React, { useEffect } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import type { Habit, HabitCreateInput } from "../../types";
import { Modal } from "../common/Modal";
import { Input } from "../common/Input";
import { Button } from "../common/Button";

const habitSchema = z.object({
  title: z
    .string()
    .min(1, "Habit title is required.")
    .max(100, "Title must not exceed 100 characters."),
  description: z.string().max(500, "Description must not exceed 500 characters.").optional(),
  category: z
    .string()
    .min(1, "Category is required.")
    .max(50, "Category must not exceed 50 characters."),
  frequency: z.enum(["daily", "weekly", "monthly"], {
    message: "Frequency must be daily, weekly, or monthly.",
  }),
});

type HabitFormValues = z.infer<typeof habitSchema>;

interface HabitFormModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (values: HabitCreateInput) => Promise<void>;
  initialData?: Habit | null;
}

export const HabitFormModal: React.FC<HabitFormModalProps> = ({
  isOpen,
  onClose,
  onSubmit,
  initialData,
}) => {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<HabitFormValues>({
    resolver: zodResolver(habitSchema),
    defaultValues: {
      title: "",
      description: "",
      category: "General",
      frequency: "daily",
    },
  });

  useEffect(() => {
    if (initialData) {
      reset({
        title: initialData.title,
        description: initialData.description || "",
        category: initialData.category,
        frequency: initialData.frequency as "daily" | "weekly" | "monthly",
      });
    } else {
      reset({
        title: "",
        description: "",
        category: "General",
        frequency: "daily",
      });
    }
  }, [initialData, isOpen, reset]);

  const handleFormSubmit = async (values: HabitFormValues) => {
    await onSubmit({
      title: values.title,
      description: values.description || undefined,
      category: values.category,
      frequency: values.frequency,
    });
    onClose();
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={initialData ? "Edit Habit" : "Create New Habit"}
    >
      <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-4">
        <Input
          label="Habit Title"
          placeholder="e.g. Morning Workout, Read 15 Pages"
          error={errors.title?.message}
          {...register("title")}
        />

        <div className="space-y-1.5 text-left">
          <label className="block text-xs font-medium text-slate-300">Description (Optional)</label>
          <textarea
            rows={3}
            placeholder="Details about your daily habit goal..."
            className="w-full px-3.5 py-2.5 bg-slate-900 border border-slate-800 rounded-xl text-slate-100 text-sm placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
            {...register("description")}
          />
          {errors.description && (
            <p className="text-xs text-rose-400">{errors.description.message}</p>
          )}
        </div>

        <div className="grid grid-cols-2 gap-4">
          <Input
            label="Category"
            placeholder="Fitness, Study, Health"
            error={errors.category?.message}
            {...register("category")}
          />

          <div className="space-y-1.5 text-left">
            <label className="block text-xs font-medium text-slate-300">Frequency</label>
            <select
              className="w-full px-3.5 py-2.5 bg-slate-900 border border-slate-800 rounded-xl text-slate-100 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              {...register("frequency")}
            >
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
              <option value="monthly">Monthly</option>
            </select>
            {errors.frequency && (
              <p className="text-xs text-rose-400">{errors.frequency.message}</p>
            )}
          </div>
        </div>

        <div className="flex justify-end space-x-3 pt-3 border-t border-slate-800">
          <Button variant="secondary" type="button" onClick={onClose} disabled={isSubmitting}>
            Cancel
          </Button>
          <Button variant="primary" type="submit" isLoading={isSubmitting}>
            {initialData ? "Save Changes" : "Create Habit"}
          </Button>
        </div>
      </form>
    </Modal>
  );
};
