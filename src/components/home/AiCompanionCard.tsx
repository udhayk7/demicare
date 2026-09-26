import React from 'react';
import { useAppState } from '../../context/AppStateContext';

export const AiCompanionCard: React.FC = () => {
  const { aiRecommendations, setActiveTab } = useAppState();

  const topRec = aiRecommendations.find(r => r.status === 'suggested') || aiRecommendations[0];

  if (!topRec) return null;

  return (
    <div className="healthcare-card p-4 space-y-2 border border-teal-200/80 bg-teal-50/30">
      <div className="flex items-center justify-between">
        <span className="text-xs font-bold text-teal-800 uppercase tracking-wider">Care Companion</span>
        <span className="text-[11px] text-teal-700 font-medium">Based on recent activity</span>
      </div>

      <div>
        <h4 className="text-sm font-bold text-slate-900 leading-snug">
          {topRec.title}
        </h4>
        <p className="text-xs text-slate-600 mt-1 leading-relaxed">
          "{topRec.reason}"
        </p>
      </div>

      <div className="flex items-center justify-between pt-2 border-t border-teal-100">
        <span className="text-xs font-semibold text-slate-500">{topRec.durationMinutes} mins</span>
        <button
          onClick={() => setActiveTab('ai-companion')}
          className="px-3 py-1.5 bg-teal-700 hover:bg-teal-800 text-white font-semibold text-xs rounded-lg transition-colors"
        >
          View suggestion
        </button>
      </div>
    </div>
  );
};
