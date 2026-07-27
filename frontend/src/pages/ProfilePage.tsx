import React from "react";
import { useAuth } from "../context/AuthContext";
import { User, Mail, Calendar, ShieldCheck } from "lucide-react";

export const ProfilePage: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-xl space-y-6 text-left">
        <div className="flex items-center space-x-4 border-b border-slate-800 pb-6">
          <div className="w-16 h-16 bg-gradient-to-br from-indigo-500 to-violet-600 rounded-2xl flex items-center justify-center text-white text-2xl font-bold shadow-lg shadow-indigo-500/20">
            {user?.username.charAt(0).toUpperCase()}
          </div>
          <div>
            <h2 className="text-2xl font-bold text-slate-100">{user?.username}</h2>
            <p className="text-sm text-slate-400">Authenticated Member</p>
          </div>
        </div>

        <div className="space-y-4">
          <div className="flex items-center space-x-3 p-3 bg-slate-950/60 border border-slate-800/80 rounded-xl">
            <User className="w-5 h-5 text-indigo-400" />
            <div>
              <p className="text-xs text-slate-500">Username</p>
              <p className="text-sm font-medium text-slate-200">{user?.username}</p>
            </div>
          </div>

          <div className="flex items-center space-x-3 p-3 bg-slate-950/60 border border-slate-800/80 rounded-xl">
            <Mail className="w-5 h-5 text-indigo-400" />
            <div>
              <p className="text-xs text-slate-500">Email Address</p>
              <p className="text-sm font-medium text-slate-200">{user?.email}</p>
            </div>
          </div>

          <div className="flex items-center space-x-3 p-3 bg-slate-950/60 border border-slate-800/80 rounded-xl">
            <Calendar className="w-5 h-5 text-indigo-400" />
            <div>
              <p className="text-xs text-slate-500">Member Since</p>
              <p className="text-sm font-medium text-slate-200">
                {user?.created_at ? new Date(user.created_at).toLocaleDateString() : "N/A"}
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-3 p-3 bg-slate-950/60 border border-slate-800/80 rounded-xl">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            <div>
              <p className="text-xs text-slate-500">Session Status</p>
              <p className="text-sm font-medium text-emerald-400">Active (JWT Bearer Verified)</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
