import React, { useState } from 'react';
import { Plus, Eye, Activity, FileText, AlertTriangle } from 'lucide-react';
import { useAppState } from '../../context/AppStateContext';

export const QuickActionsGrid: React.FC = () => {
  const { setActiveTab, simulateSOS, logBehaviourObservation, addToast } = useAppState();
  const [showLogModal, setShowLogModal] = useState(false);
  const [behaviourNote, setBehaviourNote] = useState('');
  const [obsType, setObsType] = useState<'confusion' | 'agitation' | 'repetitive_questioning' | 'wandering' | 'calm'>('confusion');
  const [intensity, setIntensity] = useState<'mild' | 'moderate' | 'severe'>('mild');

  return (
    <div className="space-y-2">
      <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider">Quick Actions</h3>

      {/* Grid of simple list action buttons */}
      <div className="grid grid-cols-2 gap-2 text-xs">
        <button
          onClick={() => setActiveTab('medication')}
          className="p-2.5 bg-white border border-slate-200 hover:border-slate-300 rounded-lg flex items-center gap-2 font-semibold text-slate-800 transition-colors"
        >
          <Plus size={15} className="text-slate-500" />
          <span>Medication</span>
        </button>

        <button
          onClick={() => setActiveTab('care')}
          className="p-2.5 bg-white border border-slate-200 hover:border-slate-300 rounded-lg flex items-center gap-2 font-semibold text-slate-800 transition-colors"
        >
          <Activity size={15} className="text-slate-500" />
          <span>Activity</span>
        </button>

        <button
          onClick={() => setShowLogModal(true)}
          className="p-2.5 bg-white border border-slate-200 hover:border-slate-300 rounded-lg flex items-center gap-2 font-semibold text-slate-800 transition-colors"
        >
          <Eye size={15} className="text-slate-500" />
          <span>Observation</span>
        </button>

        <button
          onClick={() => setActiveTab('reports')}
          className="p-2.5 bg-white border border-slate-200 hover:border-slate-300 rounded-lg flex items-center gap-2 font-semibold text-slate-800 transition-colors"
        >
          <FileText size={15} className="text-slate-500" />
          <span>Generate Report</span>
        </button>
      </div>

      {/* Separate Emergency Button */}
      <div className="pt-1">
        <button
          onClick={simulateSOS}
          className="w-full py-2.5 bg-rose-50 hover:bg-rose-100 border border-rose-200 text-rose-700 font-semibold text-xs rounded-lg flex items-center justify-center gap-1.5 transition-colors"
        >
          <AlertTriangle size={15} />
          <span>Emergency / SOS Trigger</span>
        </button>
      </div>

      {/* Log Behaviour Modal */}
      {showLogModal && (
        <div className="fixed inset-0 z-50 bg-slate-900/40 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl max-w-sm w-full p-5 space-y-3 border border-slate-200 shadow-xl">
            <h3 className="text-sm font-bold text-slate-900">Log Caregiver Observation</h3>
            <p className="text-xs text-slate-500">Record an observation regarding mood or behavior.</p>

            {/* Type selector */}
            <div className="space-y-1">
              <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">Observation Type</span>
              <div className="flex flex-wrap gap-1">
                {(['confusion', 'agitation', 'repetitive_questioning', 'wandering', 'calm'] as const).map(t => (
                  <button
                    key={t}
                    type="button"
                    onClick={() => setObsType(t)}
                    className={`px-2.5 py-1 rounded text-[11px] font-medium border capitalize ${
                      obsType === t
                        ? 'bg-sky-50 border-sky-500 text-sky-900 font-bold'
                        : 'bg-slate-50 border-slate-200 text-slate-600'
                    }`}
                  >
                    {t.replace('_', ' ')}
                  </button>
                ))}
              </div>
            </div>

            {/* Intensity selector */}
            <div className="space-y-1">
              <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">Intensity</span>
              <div className="flex gap-1.5">
                {(['mild', 'moderate', 'severe'] as const).map(i => (
                  <button
                    key={i}
                    type="button"
                    onClick={() => setIntensity(i)}
                    className={`flex-1 py-1 rounded text-[11px] font-medium border capitalize ${
                      intensity === i
                        ? 'bg-slate-900 border-slate-900 text-white font-bold'
                        : 'bg-slate-50 border-slate-200 text-slate-600'
                    }`}
                  >
                    {i}
                  </button>
                ))}
              </div>
            </div>

            <textarea
              value={behaviourNote}
              onChange={e => setBehaviourNote(e.target.value)}
              placeholder="e.g. Mild confusion during evening tea, settled quickly after reassurance."
              className="w-full text-xs p-3 border border-slate-300 rounded-lg focus:ring-1 focus:ring-sky-500 focus:outline-none min-h-[70px]"
            />

            <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
              <button
                onClick={() => setShowLogModal(false)}
                className="px-3 py-1.5 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-lg"
              >
                Cancel
              </button>
              <button
                onClick={() => {
                  if (!behaviourNote.trim()) {
                    addToast('Please enter an observation note.', 'warning');
                    return;
                  }
                  logBehaviourObservation(obsType, behaviourNote, intensity);
                  setBehaviourNote('');
                  setShowLogModal(false);
                }}
                className="px-3.5 py-1.5 text-xs font-semibold bg-sky-700 hover:bg-sky-800 text-white rounded-lg"
              >
                Save Note
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
