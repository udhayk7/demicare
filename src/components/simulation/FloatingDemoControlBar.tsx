import React, { useState } from 'react';
import { useAppState } from '../../context/AppStateContext';

export const FloatingDemoControlBar: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const {
    simulateMedicationReminder,
    simulateSOS,
    simulateGeofenceExit,
    simulateReturnHome,
    simulatePersonDetected,
    simulateUnknownPersonDetected,
    simulateGenerateNewRecommendation,
    logBehaviourObservation,
    resetSimulations
  } = useAppState();

  return (
    <div className="fixed bottom-16 right-4 z-50">
      <button
        onClick={() => setIsOpen(prev => !prev)}
        className="bg-slate-900 text-white px-3.5 py-2 rounded-lg shadow-lg text-xs font-semibold hover:bg-slate-800 transition-colors"
      >
        {isOpen ? 'Close Simulator' : '⚡ Demo Simulator'}
      </button>

      {isOpen && (
        <div className="absolute bottom-11 right-0 w-72 bg-white border border-slate-300 text-slate-800 rounded-xl p-4 shadow-2xl space-y-2.5 mb-2">
          <div className="flex items-center justify-between border-b border-slate-200 pb-2">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-900">Demo Simulator</span>
            <span className="text-[10px] text-slate-500 font-medium">Interactive</span>
          </div>

          <div className="grid grid-cols-2 gap-1.5 text-xs">
            <button
              onClick={() => {
                simulateMedicationReminder();
                setIsOpen(false);
              }}
              className="p-2 bg-amber-50 hover:bg-amber-100 text-amber-900 font-medium border border-amber-200 rounded-lg text-left"
            >
              Med Reminder
            </button>

            <button
              onClick={() => {
                simulateSOS();
                setIsOpen(false);
              }}
              className="p-2 bg-rose-50 hover:bg-rose-100 text-rose-900 font-medium border border-rose-200 rounded-lg text-left"
            >
              Trigger SOS
            </button>

            <button
              onClick={() => {
                simulateGeofenceExit();
                setIsOpen(false);
              }}
              className="p-2 bg-slate-100 hover:bg-slate-200 text-slate-800 font-medium rounded-lg text-left"
            >
              Safe Zone Exit
            </button>

            <button
              onClick={() => {
                simulateReturnHome();
                setIsOpen(false);
              }}
              className="p-2 bg-emerald-50 hover:bg-emerald-100 text-emerald-900 font-medium border border-emerald-200 rounded-lg text-left"
            >
              Return Home
            </button>

            <button
              onClick={() => {
                simulatePersonDetected('Anu Menon', 'Daughter');
                setIsOpen(false);
              }}
              className="p-2 bg-slate-100 hover:bg-slate-200 text-slate-800 font-medium rounded-lg text-left"
            >
              Cam: Daughter
            </button>

            <button
              onClick={() => {
                simulateUnknownPersonDetected();
                setIsOpen(false);
              }}
              className="p-2 bg-slate-100 hover:bg-slate-200 text-slate-800 font-medium rounded-lg text-left"
            >
              Cam: Unknown
            </button>

            <button
              onClick={() => {
                simulateGenerateNewRecommendation();
                setIsOpen(false);
              }}
              className="p-2 bg-teal-50 hover:bg-teal-100 text-teal-900 font-medium border border-teal-200 rounded-lg text-left"
            >
              New AI Rec
            </button>

            <button
              onClick={() => {
                logBehaviourObservation('confusion', 'Slight disorientation during tea time.', 'mild');
                setIsOpen(false);
              }}
              className="p-2 bg-slate-100 hover:bg-slate-200 text-slate-800 font-medium rounded-lg text-left"
            >
              Log Confusion
            </button>
          </div>

          <div className="pt-2 border-t border-slate-100 flex justify-between items-center text-[11px]">
            <button
              onClick={() => {
                resetSimulations();
                setIsOpen(false);
              }}
              className="text-slate-500 hover:text-slate-900 font-medium underline"
            >
              Reset State
            </button>
            <span className="text-slate-400">CareCompanion Demo</span>
          </div>
        </div>
      )}
    </div>
  );
};
