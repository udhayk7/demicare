import React from 'react';
import { useAppState } from '../../context/AppStateContext';

export const AttentionCard: React.FC = () => {
  const { medications, setActiveTab, markMedicationTaken, patient } = useAppState();

  const pendingMed = medications.find(m => m.status === 'pending' || m.status === 'missed');

  if (!pendingMed && patient.status === 'stable') {
    return null;
  }

  return (
    <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-xs font-bold text-amber-900 uppercase tracking-wider">Needs your attention</span>
        {pendingMed && <span className="text-[11px] font-semibold text-amber-800">{pendingMed.scheduledTime}</span>}
      </div>

      <div>
        <h3 className="text-sm font-bold text-slate-900">
          {pendingMed ? "Medication hasn't been acknowledged" : "Patient Status Attention Required"}
        </h3>
        <p className="text-xs text-amber-900/80 mt-0.5">
          {pendingMed
            ? `${pendingMed.name} (${pendingMed.dosage}) scheduled for ${pendingMed.scheduledTime}`
            : "Review patient location, safety notifications, or routine observations."}
        </p>
      </div>

      <div className="flex items-center justify-end gap-2 pt-2 border-t border-amber-200/60">
        <button
          onClick={() => setActiveTab(pendingMed ? 'medication' : 'monitor')}
          className="px-3 py-1.5 text-xs font-semibold text-amber-900 hover:bg-amber-100/80 rounded-lg transition-colors"
        >
          {pendingMed ? 'View medication' : 'Check status'}
        </button>
        {pendingMed && (
          <button
            onClick={() => markMedicationTaken(pendingMed.id)}
            className="px-3.5 py-1.5 bg-amber-700 hover:bg-amber-800 text-white font-semibold text-xs rounded-lg transition-colors"
          >
            Mark taken
          </button>
        )}
      </div>
    </div>
  );
};
