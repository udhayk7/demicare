import React from 'react';
import { useAppState } from '../../context/AppStateContext';

export const NextUpCard: React.FC = () => {
  const { setActiveTab } = useAppState();

  return (
    <div className="healthcare-card p-4 flex items-center justify-between">
      <div>
        <span className="text-xs font-bold text-slate-500 uppercase tracking-wider block mb-0.5">Next</span>
        <h4 className="text-sm font-bold text-slate-900">Donepezil 5 mg</h4>
        <p className="text-xs text-slate-500 font-medium">Scheduled for 9:00 PM</p>
      </div>

      <button
        onClick={() => setActiveTab('medication')}
        className="px-3.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs rounded-lg transition-colors"
      >
        View
      </button>
    </div>
  );
};
