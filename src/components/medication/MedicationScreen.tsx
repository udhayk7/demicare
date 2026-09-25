import React from 'react';
import { useAppState } from '../../context/AppStateContext';

export const MedicationScreen: React.FC = () => {
  const { medications, markMedicationTaken, markMedicationMissed } = useAppState();

  const takenCount = medications.filter(m => m.status === 'taken').length;
  const totalMeds = medications.length;
  const adherencePercent = Math.round((takenCount / (totalMeds || 1)) * 100);

  return (
    <div className="p-4 space-y-4 pb-20">
      {/* Page Title & Context Header */}
      <div>
        <h2 className="text-base font-bold text-slate-900">Medication Schedule</h2>
        <p className="text-xs text-slate-500 font-medium">
          Monthly adherence: {adherencePercent}% ({takenCount} of {totalMeds} doses acknowledged today)
        </p>
      </div>

      {/* Clean Medication List Rows */}
      <div className="healthcare-section divide-y divide-slate-100">
        {medications.map(med => {
          const isTaken = med.status === 'taken';
          const isMissed = med.status === 'missed';

          return (
            <div key={med.id} className="p-4 space-y-1.5">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-900">{med.scheduledTime}</span>
                <span
                  className={`text-xs font-semibold ${
                    isTaken ? 'text-emerald-700' : isMissed ? 'text-rose-700' : 'text-amber-700'
                  }`}
                >
                  {isTaken ? '✓ Taken' : isMissed ? '● Missed' : '● Needs attention'}
                </span>
              </div>

              <div>
                <h4 className="text-sm font-bold text-slate-900">{med.name} {med.dosage}</h4>
                <p className="text-xs text-slate-500">{med.instructions}</p>
              </div>

              {!isTaken && (
                <div className="flex items-center justify-end gap-2 pt-2">
                  {isMissed ? (
                    <button
                      onClick={() => markMedicationTaken(med.id)}
                      className="px-3 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs rounded-lg transition-colors"
                    >
                      Mark taken late
                    </button>
                  ) : (
                    <>
                      <button
                        onClick={() => markMedicationMissed(med.id)}
                        className="px-3 py-1 text-slate-500 hover:text-rose-700 font-semibold text-xs transition-colors"
                      >
                        Mark missed
                      </button>
                      <button
                        onClick={() => markMedicationTaken(med.id)}
                        className="px-3.5 py-1.5 bg-emerald-700 hover:bg-emerald-800 text-white font-semibold text-xs rounded-lg transition-colors"
                      >
                        Confirm taken
                      </button>
                    </>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
