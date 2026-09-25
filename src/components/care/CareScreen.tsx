import React, { useState } from 'react';
import { useAppState } from '../../context/AppStateContext';

export const CareScreen: React.FC = () => {
  const {
    routines,
    habilitation,
    cognitive,
    toggleHabilitation,
    toggleCognitive,
    setActiveTab
  } = useAppState();

  const [activeSubSection, setActiveSubSection] = useState<'overview' | 'habilitation' | 'cognitive'>('overview');

  const med = routines.find(r => r.category === 'medication') || { completed: 4, total: 5 };
  const habCount = habilitation.filter(h => h.completed).length;
  const habTotal = habilitation.length;
  const habPct = Math.round((habCount / (habTotal || 1)) * 100);

  const cogCount = cognitive.filter(c => c.completed).length;
  const cogTotal = cognitive.length;

  return (
    <div className="p-4 space-y-4 pb-20">
      {/* Header */}
      <div>
        <h2 className="text-base font-bold text-slate-900">Care Plan & Routines</h2>
        <p className="text-xs text-slate-500 font-medium">Daily care activities, habilitation, and cognitive exercises</p>
      </div>

      {/* Sub-tab Pill Switcher */}
      <div className="flex bg-slate-200/60 p-1 rounded-lg text-xs font-semibold">
        <button
          onClick={() => setActiveSubSection('overview')}
          className={`flex-1 py-1.5 rounded transition-all ${
            activeSubSection === 'overview' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'
          }`}
        >
          Overview
        </button>
        <button
          onClick={() => setActiveSubSection('habilitation')}
          className={`flex-1 py-1.5 rounded transition-all ${
            activeSubSection === 'habilitation' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'
          }`}
        >
          Habilitation ({habCount}/{habTotal})
        </button>
        <button
          onClick={() => setActiveSubSection('cognitive')}
          className={`flex-1 py-1.5 rounded transition-all ${
            activeSubSection === 'cognitive' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-600 hover:text-slate-900'
          }`}
        >
          Cognitive ({cogCount}/{cogTotal})
        </button>
      </div>

      {activeSubSection === 'overview' && (
        <div className="healthcare-section divide-y divide-slate-100">
          <div onClick={() => setActiveTab('medication')} className="p-4 flex items-center justify-between cursor-pointer hover:bg-slate-50">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Medication</h3>
              <p className="text-xs text-slate-500">{med.completed} of {med.total} doses completed</p>
            </div>
            <span className="text-xs font-semibold text-sky-700">View</span>
          </div>

          <div onClick={() => setActiveSubSection('habilitation')} className="p-4 flex items-center justify-between cursor-pointer hover:bg-slate-50">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Habilitation</h3>
              <p className="text-xs text-slate-500">{habPct}% adherence ({habCount} of {habTotal} completed)</p>
            </div>
            <span className="text-xs font-semibold text-sky-700">View</span>
          </div>

          <div onClick={() => setActiveSubSection('cognitive')} className="p-4 flex items-center justify-between cursor-pointer hover:bg-slate-50">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Cognitive Tasks</h3>
              <p className="text-xs text-slate-500">{cogCount} of {cogTotal} completed</p>
            </div>
            <span className="text-xs font-semibold text-sky-700">View</span>
          </div>

          <div className="p-4 flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Nutrition & Meals</h3>
              <p className="text-xs text-slate-500">3 meals logged today</p>
            </div>
            <span className="text-xs font-semibold text-emerald-700">Completed</span>
          </div>

          <div className="p-4 flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Hydration</h3>
              <p className="text-xs text-slate-500">5 of 7 glasses logged</p>
            </div>
            <span className="text-xs font-semibold text-slate-600">Pending</span>
          </div>
        </div>
      )}

      {activeSubSection === 'habilitation' && (
        <div className="healthcare-section divide-y divide-slate-100">
          {habilitation.map(hab => (
            <div
              key={hab.id}
              onClick={() => toggleHabilitation(hab.id)}
              className="p-4 flex items-center justify-between cursor-pointer hover:bg-slate-50"
            >
              <div>
                <h4 className={`text-sm font-bold ${hab.completed ? 'line-through text-slate-400' : 'text-slate-900'}`}>
                  {hab.title}
                </h4>
                <p className="text-xs text-slate-500">{hab.category} · {hab.durationMinutes} mins · Scheduled {hab.scheduledTime}</p>
              </div>
              <span className={`text-xs font-semibold ${hab.completed ? 'text-emerald-700' : 'text-slate-600'}`}>
                {hab.completed ? '✓ Completed' : 'Pending'}
              </span>
            </div>
          ))}
        </div>
      )}

      {activeSubSection === 'cognitive' && (
        <div className="healthcare-section divide-y divide-slate-100">
          {cognitive.map(cog => (
            <div
              key={cog.id}
              onClick={() => toggleCognitive(cog.id)}
              className="p-4 flex items-center justify-between cursor-pointer hover:bg-slate-50"
            >
              <div>
                <h4 className={`text-sm font-bold ${cog.completed ? 'line-through text-slate-400' : 'text-slate-900'}`}>
                  {cog.title}
                </h4>
                <p className="text-xs text-slate-500">{cog.type} · {cog.durationMinutes} mins {cog.score ? `· ${cog.score}` : ''}</p>
              </div>
              <span className={`text-xs font-semibold ${cog.completed ? 'text-emerald-700' : 'text-slate-600'}`}>
                {cog.completed ? '✓ Completed' : 'Pending'}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
