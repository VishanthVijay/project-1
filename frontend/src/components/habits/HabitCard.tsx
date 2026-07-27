import React from "react";
import type { Habit, HabitStats } from "../../types";
import { Flame, CheckCircle2, Circle, Edit2, Trash2, Calendar, Trophy } from "lucide-react";
import { Button } from "../common/Button";

interface HabitCardProps {
  habit: Habit;
  stats?: HabitStats;
  isCompletedToday: boolean;
  onToggleComplete: (habitId: number) => void;
  onEdit: (habit: Habit) => void;
  onDelete: (habitId: number) => void;
}

export const HabitCard: React.FC<HabitCardProps> = ({
  habit,
  stats,
  isCompletedToday,
  onToggleComplete,
  onEdit,
  onDelete,
}) => {
  return (
    <div className="bg-slate-900 border border-slate-800 hover:border-slate-700/80 rounded-2xl p-5 shadow-lg flex flex-col justify-between transition-all duration-200 group">
      {/* Top Header */}
      <div className="space-y-3">
        <div className="flex items-start justify-between">
          <div>
            <span className="inline-block px-2.5 py-1 text-[11px] font-semibold text-indigo-400 bg-indigo-500/10 rounded-lg uppercase tracking-wider mb-2">
              {habit.category}
            </span>
            <h3 className="text-lg font-bold text-slate-100 group-hover:text-indigo-300 transition-colors">
              {habit.title}
            </h3>
          </div>
          <div className="flex items-center space-x-1 opacity-80 group-hover:opacity-100 transition-opacity">
            <button
              onClick={() => onEdit(habit)}
              className="p-1.5 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-lg transition-colors"
              title="Edit habit"
            >
              <Edit2 className="w-4 h-4" />
            </button>
            <button
              onClick={() => onDelete(habit.id)}
              className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 rounded-lg transition-colors"
              title="Delete habit"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        </div>

        {habit.description && (
          <p className="text-sm text-slate-400 line-clamp-2">{habit.description}</p>
        )}
      </div>

      {/* Streak Stats Grid */}
      <div className="grid grid-cols-2 gap-2 my-4 p-3 bg-slate-950/60 rounded-xl border border-slate-800/60 text-xs">
        <div className="flex items-center space-x-2">
          <div className="p-1.5 bg-amber-500/10 text-amber-400 rounded-lg">
            <Flame className="w-4 h-4" />
          </div>
          <div>
            <p className="text-slate-500 text-[10px]">Current Streak</p>
            <p className="font-bold text-slate-200">{stats?.current_streak ?? 0} days</p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <div className="p-1.5 bg-violet-500/10 text-violet-400 rounded-lg">
            <Trophy className="w-4 h-4" />
          </div>
          <div>
            <p className="text-slate-500 text-[10px]">Best Streak</p>
            <p className="font-bold text-slate-200">{stats?.longest_streak ?? 0} days</p>
          </div>
        </div>
      </div>

      {/* Action Footer */}
      <div className="pt-2 flex items-center justify-between border-t border-slate-800/60">
        <span className="text-xs text-slate-500 flex items-center gap-1">
          <Calendar className="w-3.5 h-3.5" />
          {habit.frequency}
        </span>

        <Button
          onClick={() => onToggleComplete(habit.id)}
          variant={isCompletedToday ? "secondary" : "primary"}
          size="sm"
          className={
            isCompletedToday
              ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/30 hover:bg-emerald-500/20"
              : ""
          }
        >
          {isCompletedToday ? (
            <>
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              Completed Today
            </>
          ) : (
            <>
              <Circle className="w-4 h-4" />
              Mark Complete
            </>
          )}
        </Button>
      </div>
    </div>
  );
};
