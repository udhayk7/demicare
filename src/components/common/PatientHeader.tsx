import React from 'react';
import { Bell, Smartphone, Monitor } from 'lucide-react';
import { useAppState } from '../../context/AppStateContext';
import { StatusBadge } from './StatusBadge';

export const PatientHeader: React.FC = () => {
  const { patient, notifications, isPhoneFrame, setIsPhoneFrame, setActiveTab } = useAppState();
  const unreadCount = notifications.filter(n => !n.read).length;

  return (
    <header className="bg-white sticky top-0 z-30 px-4 py-3 border-b border-slate-200">
      <div className="flex items-center justify-between gap-3">
        {/* Patient Identity & Caregiver Context */}
        <div className="flex items-center gap-3">
          <img
            src={patient.avatarUrl}
            alt={patient.name}
            className="w-10 h-10 rounded-full object-cover border border-slate-200"
          />
          <div>
            <div className="text-xs text-slate-500 font-medium">
              Good morning, {patient.primaryCaregiver.split(' ')[0]}
            </div>
            <div className="flex items-center gap-2 mt-0.5">
              <h1 className="text-base font-bold text-slate-900 leading-tight">
                Caring for {patient.name.split(' ')[0]}
              </h1>
              <span className="text-slate-300">•</span>
              <StatusBadge status={patient.status} size="sm" />
            </div>
          </div>
        </div>

        {/* Action icons */}
        <div className="flex items-center gap-1">
          <button
            onClick={() => setIsPhoneFrame(prev => !prev)}
            title={isPhoneFrame ? 'Switch to Full View' : 'Switch to Phone View'}
            className="p-2 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors hidden sm:flex items-center justify-center"
          >
            {isPhoneFrame ? <Monitor size={17} /> : <Smartphone size={17} />}
          </button>

          <button
            onClick={() => setActiveTab('timeline')}
            className="relative p-2 rounded-lg text-slate-500 hover:text-slate-800 hover:bg-slate-100 transition-colors"
            title="Notifications & Timeline"
          >
            <Bell size={18} />
            {unreadCount > 0 && (
              <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-rose-600 rounded-full" />
            )}
          </button>
        </div>
      </div>
    </header>
  );
};
