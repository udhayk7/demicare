import React from 'react';
import { useAppState } from '../../context/AppStateContext';

export const PatientStatusCard: React.FC = () => {
  const { location, movement, sleep, pendant, patient, setActiveTab } = useAppState();

  const isAtHome = location.status === 'at_home';

  return (
    <div className="healthcare-section p-4 space-y-3">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xs font-bold text-slate-500 uppercase tracking-wider">Patient Status</h2>
          <p className="text-sm font-bold text-slate-900 mt-0.5">
            {isAtHome ? `${patient.name.split(' ')[0]} is doing well today` : `${patient.name.split(' ')[0]} requires location check`}
          </p>
        </div>
        <span className="text-[11px] text-slate-400 font-medium">Updated {location.lastUpdated}</span>
      </div>

      <div className="divide-y divide-slate-100 text-xs text-slate-700 pt-1">
        <div className="py-2 flex items-center justify-between">
          <span className="font-medium text-slate-600">Location</span>
          <span className={`font-semibold flex items-center gap-1.5 ${isAtHome ? 'text-emerald-700' : 'text-rose-600'}`}>
            <span className={`w-2 h-2 rounded-full ${isAtHome ? 'bg-emerald-500' : 'bg-rose-600'}`} />
            <span>{isAtHome ? 'At home' : 'Exited safe zone'}</span>
          </span>
        </div>

        <div className="py-2 flex items-center justify-between">
          <span className="font-medium text-slate-600">Movement</span>
          <span className="font-semibold text-slate-900">{movement.dailyKm} km today</span>
        </div>

        <div className="py-2 flex items-center justify-between">
          <span className="font-medium text-slate-600">Sleep</span>
          <span className="font-semibold text-slate-900">{sleep.durationHours}h last night</span>
        </div>

        <div className="py-2 flex items-center justify-between">
          <span className="font-medium text-slate-600">Pendant</span>
          <span className={`font-semibold flex items-center gap-1.5 ${pendant.batteryLevel <= 20 ? 'text-amber-700' : 'text-slate-900'}`}>
            <span className={`w-2 h-2 rounded-full ${!pendant.connected ? 'bg-slate-400' : pendant.batteryLevel <= 20 ? 'bg-amber-500 animate-pulse' : 'bg-emerald-500'}`} />
            <span>{pendant.connected ? `Connected (${pendant.batteryLevel}%${pendant.batteryLevel <= 20 ? ' · Low' : ''})` : 'Disconnected'}</span>
          </span>
        </div>
      </div>

      <div className="pt-2 border-t border-slate-100 text-right">
        <button
          onClick={() => setActiveTab('monitor')}
          className="text-xs font-semibold text-sky-700 hover:text-sky-900"
        >
          View monitoring dashboard
        </button>
      </div>
    </div>
  );
};
