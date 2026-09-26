import React from 'react';
import { useAppState } from '../../context/AppStateContext';

export const MonitorScreen: React.FC = () => {
  const {
    location,
    movement,
    sleep,
    pendant,
    safetyEvents,
    simulateSOS,
    simulateGeofenceExit,
    simulateReturnHome,
    resolveSafetyAlert,
    addToast
  } = useAppState();

  const isAtHome = location.status === 'at_home';
  const activeSafety = safetyEvents.find(s => !s.resolved);

  return (
    <div className="w-full max-w-4xl mx-auto p-4 sm:p-6 lg:p-8 space-y-4 md:space-y-6 pb-[calc(5.5rem+env(safe-area-inset-bottom,0px))] md:pb-12">
      {/* Header */}
      <div>
        <div className="flex items-center justify-between">
          <h2 className="text-base font-bold text-slate-900">Patient Monitoring</h2>
          <span className="text-[10px] bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-medium">
            Simulated IoT Gateway
          </span>
        </div>
        <p className="text-xs text-slate-500 font-medium">Real-time location, pendant diagnostic & status overview</p>
      </div>

      {/* Immediate State Status Banner (Section 9) */}
      <div className={`p-3 rounded-xl border flex items-center justify-between text-xs transition-colors ${
        isAtHome && !activeSafety && pendant.batteryLevel > 15
          ? 'bg-emerald-50 border-emerald-200 text-emerald-900'
          : 'bg-rose-50 border-rose-200 text-rose-900'
      }`}>
        <div className="flex items-center gap-2">
          <span className={`w-2.5 h-2.5 rounded-full ${
            isAtHome && !activeSafety && pendant.batteryLevel > 15
              ? 'bg-emerald-500'
              : 'bg-rose-600 animate-pulse'
          }`} />
          <span className="font-bold">
            {isAtHome && !activeSafety && pendant.batteryLevel > 15
              ? 'SAFE · Inside 150m Safe Zone · Normal'
              : !isAtHome
              ? 'ATTENTION · Patient Outside Safe Zone'
              : activeSafety
              ? `CRITICAL ALERT · ${activeSafety.type === 'sos_button' ? 'SOS Active' : 'Safety Warning'}`
              : 'ATTENTION · Low Pendant Battery'}
          </span>
        </div>
        {activeSafety && (
          <button
            onClick={resolveSafetyAlert}
            className="px-2.5 py-1 bg-white hover:bg-rose-100 text-rose-800 text-[11px] font-bold rounded-lg border border-rose-300 shadow-xs"
          >
            Resolve
          </button>
        )}
      </div>

      {/* Overview Section */}
      <div className="healthcare-section divide-y divide-slate-100">
        <div className="p-3.5 flex items-center justify-between">
          <span className="text-xs font-medium text-slate-600">Location</span>
          <span className={`text-xs font-semibold flex items-center gap-1.5 ${isAtHome ? 'text-emerald-700' : 'text-rose-600'}`}>
            <span className={`w-2 h-2 rounded-full ${isAtHome ? 'bg-emerald-500' : 'bg-rose-600'}`} />
            <span>{isAtHome ? 'At home' : 'Exited safe zone'}</span>
          </span>
        </div>

        <div className="p-3.5 flex items-center justify-between text-xs">
          <span className="font-medium text-slate-600">Movement</span>
          <span className="font-semibold text-slate-900">{movement.dailyKm} km today ({movement.steps.toLocaleString()} steps)</span>
        </div>

        <div className="p-3.5 flex items-center justify-between text-xs">
          <span className="font-medium text-slate-600">Sleep</span>
          <span className="font-semibold text-slate-900">{sleep.durationHours}h last night ({sleep.quality})</span>
        </div>

        <div className="p-3.5 flex items-center justify-between text-xs">
          <span className="font-medium text-slate-600">Safety</span>
          {activeSafety ? (
            <div className="flex items-center gap-2">
              <span className="font-semibold text-rose-600 flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-rose-600 animate-pulse" />
                <span>{activeSafety.type === 'sos_button' ? 'Emergency SOS' : 'Safe-Zone Alert'}</span>
              </span>
              <button
                onClick={resolveSafetyAlert}
                className="px-2 py-0.5 bg-rose-100 hover:bg-rose-200 text-rose-800 text-[10px] font-bold rounded"
              >
                Resolve
              </button>
            </div>
          ) : (
            <span className="font-semibold text-emerald-700 flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-500" />
              <span>No active alerts</span>
            </span>
          )}
        </div>

        <div className="p-3.5 flex items-center justify-between text-xs">
          <span className="font-medium text-slate-600">Pendant</span>
          <span className={`font-semibold flex items-center gap-1.5 ${pendant.batteryLevel <= 15 ? 'text-amber-600' : 'text-slate-900'}`}>
            <span className={`w-2 h-2 rounded-full ${pendant.batteryLevel <= 15 ? 'bg-amber-500 animate-pulse' : 'bg-emerald-500'}`} />
            <span>Connected ({pendant.batteryLevel}% battery{pendant.batteryLevel <= 15 ? ' - Low' : ''})</span>
          </span>
        </div>
      </div>

      {/* Practical Map Tool Section */}
      <div className="healthcare-section p-4 space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider">Safe Zone & Map</h3>
          <span className="text-[11px] text-slate-400">Updated {location.lastUpdated}</span>
        </div>

        {/* Clean map area */}
        <div className="w-full h-40 bg-slate-100 rounded-lg border border-slate-200 relative overflow-hidden flex items-center justify-center">
          {/* Subtle grid */}
          <div className="absolute inset-0 opacity-15 bg-[radial-gradient(#64748b_1px,transparent_1px)] [background-size:16px_16px]" />

          {/* Safe zone boundary */}
          <div className="w-32 h-32 rounded-full border-2 border-emerald-500/50 bg-emerald-500/10 flex items-center justify-center">
            <span className="text-[10px] text-emerald-800 font-bold bg-white px-2 py-0.5 rounded border border-emerald-200 shadow-xs">
              150m Safe Zone
            </span>
          </div>

          {/* Patient location pin */}
          <div className={`absolute flex items-center gap-1 bg-white px-2 py-1 rounded border border-slate-300 shadow-xs text-xs font-bold ${
            isAtHome ? 'translate-x-0' : 'translate-x-20 -translate-y-8'
          }`}>
            <span className={`w-2 h-2 rounded-full ${isAtHome ? 'bg-emerald-500' : 'bg-rose-600'}`} />
            <span>Raghavan</span>
          </div>
        </div>

        <div className="flex items-center justify-between text-xs pt-1">
          <span className="text-slate-600">{location.address}</span>
          {isAtHome ? (
            <button
              onClick={simulateGeofenceExit}
              className="px-3 py-1 bg-rose-50 hover:bg-rose-100 text-rose-700 font-semibold rounded-lg border border-rose-200 transition-colors"
            >
              Simulate exit
            </button>
          ) : (
            <button
              onClick={simulateReturnHome}
              className="px-3 py-1 bg-emerald-700 hover:bg-emerald-800 text-white font-semibold rounded-lg transition-colors"
            >
              Return home
            </button>
          )}
        </div>
      </div>

      {/* Pendant Device Information */}
      <div className="healthcare-section p-4 space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider">Raghavan's Pendant</h3>
          <span className="text-xs font-semibold text-emerald-700 flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
            Connected
          </span>
        </div>

        <div className="divide-y divide-slate-100 text-xs">
          <div className="py-2 flex items-center justify-between">
            <span className="text-slate-600">Battery level</span>
            <span className="font-semibold text-slate-900">{pendant.batteryLevel}%</span>
          </div>

          <div className="py-2 flex items-center justify-between">
            <span className="text-slate-600">GPS Status</span>
            <span className="font-semibold text-emerald-700">Available</span>
          </div>

          <div className="py-2 flex items-center justify-between">
            <span className="text-slate-600">Speaker Status</span>
            <span className="font-semibold text-emerald-700">Available</span>
          </div>

          <div className="py-2 flex items-center justify-between">
            <span className="text-slate-600">Last synced</span>
            <span className="font-medium text-slate-500">{pendant.lastSync}</span>
          </div>
        </div>

        <div className="flex items-center gap-2 pt-2 border-t border-slate-100">
          <button
            onClick={() => addToast('Test reminder tone played on pendant.', 'info')}
            className="flex-1 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs rounded-lg transition-colors text-center"
          >
            Test reminder
          </button>
          <button
            onClick={simulateSOS}
            className="flex-1 py-1.5 bg-rose-50 hover:bg-rose-100 text-rose-700 font-semibold text-xs rounded-lg border border-rose-200 transition-colors text-center"
          >
            Simulate SOS
          </button>
        </div>
      </div>
    </div>
  );
};
