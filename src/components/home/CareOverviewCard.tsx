import React from 'react';
import { useAppState } from '../../context/AppStateContext';

export const CareOverviewCard: React.FC = () => {
  const { routines, setActiveTab } = useAppState();

  const med = routines.find(r => r.category === 'medication') || { completed: 4, total: 5 };
  const act = routines.find(r => r.category === 'activities') || { completed: 6, total: 7 };
  const cog = routines.find(r => r.category === 'cognitive') || { completed: 2, total: 3 };
  const hyd = routines.find(r => r.category === 'hydration') || { completed: 5, total: 7 };

  return (
    <div className="healthcare-section p-4 space-y-3">
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-1.5">
            <h2 className="text-xs font-bold text-slate-500 uppercase tracking-wider">Today's Care</h2>
            <span className="text-[10px] bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded font-medium">Caregiver-First Plan</span>
          </div>
          <p className="text-sm font-bold text-slate-900 mt-0.5">Most care activities are on track</p>
        </div>
        <button
          onClick={() => setActiveTab('care')}
          className="text-xs font-semibold text-sky-700 hover:text-sky-900"
        >
          View all
        </button>
      </div>

      {/* Rows with thin horizontal dividers */}
      <div className="divide-y divide-slate-100 text-xs text-slate-700 pt-1">
        <div className="py-2.5 flex items-center justify-between">
          <span className="font-medium text-slate-800">Medications</span>
          <span className="font-semibold text-slate-900">{med.completed} of {med.total} taken</span>
        </div>

        <div className="py-2.5 flex items-center justify-between">
          <span className="font-medium text-slate-800">Daily care activities</span>
          <span className="font-semibold text-slate-900">{act.completed} of {act.total} completed</span>
        </div>

        <div className="py-2.5 flex items-center justify-between">
          <span className="font-medium text-slate-800">Cognitive exercises</span>
          <span className="font-semibold text-slate-900">{cog.completed} of {cog.total} completed</span>
        </div>

        <div className="py-2.5 flex items-center justify-between">
          <span className="font-medium text-slate-800">Hydration</span>
          <span className="font-semibold text-slate-900">{hyd.completed} of {hyd.total} glasses</span>
        </div>
      </div>
    </div>
  );
};
