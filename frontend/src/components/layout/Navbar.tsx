import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { Activity, LogOut, User as UserIcon } from "lucide-react";

export const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-800 bg-slate-950/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <Link to="/" className="flex items-center space-x-2 text-indigo-400 font-bold text-lg hover:opacity-90">
          <div className="p-2 bg-indigo-500/10 rounded-xl">
            <Activity className="w-5 h-5" />
          </div>
          <span className="bg-gradient-to-r from-indigo-400 to-violet-400 bg-clip-text text-transparent">
            Habit Tracker
          </span>
        </Link>

        {/* User Info & Actions */}
        {user ? (
          <div className="flex items-center space-x-4">
            <Link
              to="/profile"
              className="flex items-center space-x-2 text-slate-300 hover:text-white px-3 py-1.5 rounded-lg hover:bg-slate-900 transition-colors text-sm"
            >
              <UserIcon className="w-4 h-4 text-indigo-400" />
              <span>{user.username}</span>
            </Link>
            <button
              onClick={handleLogout}
              className="flex items-center space-x-1.5 text-xs text-slate-400 hover:text-rose-400 px-3 py-1.5 rounded-lg hover:bg-slate-900 transition-colors"
            >
              <LogOut className="w-4 h-4" />
              <span>Logout</span>
            </button>
          </div>
        ) : (
          <div className="flex items-center space-x-3 text-sm">
            <Link to="/login" className="text-slate-300 hover:text-white px-3 py-1.5">
              Login
            </Link>
            <Link
              to="/register"
              className="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-1.5 rounded-xl font-medium"
            >
              Get Started
            </Link>
          </div>
        )}
      </div>
    </header>
  );
};
