import React from 'react';
import { useAppState } from '../../context/AppStateContext';

export const InsightsScreen: React.FC = () => {
  const { aiInsights } = useAppState();

  const metrics = [
    { label: 'Care adherence', value: '87%', status: 'Most tasks on track' },
    { label: 'Medication', value: '91%', status: 'High consistency' },
    { label: 'Habilitation', value: '83%', status: 'Regular participation' },
    { label: 'Cognitive exercises', value: '86%', status: 'Stable completion' },
    { label: 'Hydration', value: '78%', status: '5 of 7 glasses avg' },
    { label: 'Sleep average', value: '7.3h', status: 'Restful night sleep' },
    { label: 'Movement', value: '3.1 km/d', status: 'Normal daily walk' }
  ];

  return (
    <div className="p-4 space-y-4 pb-20">
      {/* Header */}
      <div>
        <h2 className="text-base font-bold text-slate-900">Care Insights</h2>
        <p className="text-xs text-slate-500 font-medium">Care adherence summary & recent observations</p>
      </div>

      {/* Overview section */}
      <div className="healthcare-section p-4 space-y-2">
        <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block">Weekly Care Summary</span>
        <div className="flex items-baseline gap-2">
          <span className="text-2xl font-bold text-slate-900">87%</span>
          <span className="text-xs font-semibold text-emerald-700">Overall care adherence</span>
        </div>
        <p className="text-xs text-slate-600 leading-relaxed">
          Raghavan has maintained high routine consistency this week with stable sleep and regular outdoor balcony walks.
        </p>
      </div>

      {/* Routine breakdown list rows */}
      <div className="healthcare-section divide-y divide-slate-100">
        {metrics.map(m => (
          <div key={m.label} className="p-3.5 flex items-center justify-between text-xs">
            <div>
              <span className="font-semibold text-slate-800 block">{m.label}</span>
              <span className="text-slate-500 text-[11px]">{m.status}</span>
            </div>
            <span className="font-bold text-slate-900 text-sm">{m.value}</span>
          </div>
        ))}
      </div>

      {/* Observations */}
      <div className="space-y-2">
        <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider">Observed Insights</h3>
        <div className="healthcare-section divide-y divide-slate-100">
          {aiInsights.map(ins => (
            <div key={ins.id} className="p-4 space-y-1">
              <div className="flex items-center justify-between text-xs">
                <span className="font-bold text-slate-900">{ins.title}</span>
                <span className="text-[11px] text-slate-400">{ins.timestamp}</span>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed">{ins.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
