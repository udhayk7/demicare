import React from 'react';
import { useAppState } from '../../context/AppStateContext';
import { CheckCircle2, AlertTriangle, Info, AlertCircle, X } from 'lucide-react';

export const ToastContainer: React.FC = () => {
  const { toasts, removeToast } = useAppState();

  if (toasts.length === 0) return null;

  return (
    <div className="fixed top-4 right-4 left-4 sm:left-auto sm:w-96 z-50 flex flex-col gap-2 pointer-events-none">
      {toasts.map(toast => {
        let bgClass = 'bg-slate-900 text-white border-slate-700';
        let Icon = Info;

        if (toast.type === 'success') {
          bgClass = 'bg-emerald-900/95 text-emerald-100 border-emerald-700/60 shadow-emerald-950/20';
          Icon = CheckCircle2;
        } else if (toast.type === 'warning') {
          bgClass = 'bg-amber-950/95 text-amber-100 border-amber-700/60 shadow-amber-950/20';
          Icon = AlertTriangle;
        } else if (toast.type === 'alert') {
          bgClass = 'bg-rose-950/95 text-rose-100 border-rose-700/60 shadow-rose-950/30 animate-bounce';
          Icon = AlertCircle;
        }

        return (
          <div
            key={toast.id}
            className={`pointer-events-auto flex items-start justify-between gap-3 px-4 py-3 rounded-2xl border backdrop-blur-md shadow-lg text-xs sm:text-sm font-medium transition-all duration-300 transform translate-y-0 ${bgClass}`}
          >
            <div className="flex items-center gap-2.5">
              <Icon size={18} className="shrink-0 mt-0.5" />
              <p className="leading-snug">{toast.message}</p>
            </div>
            <button
              onClick={() => removeToast(toast.id)}
              className="text-white/60 hover:text-white p-0.5 rounded-lg transition-colors"
            >
              <X size={14} />
            </button>
          </div>
        );
      })}
    </div>
  );
};
