import React from 'react';
import { useAppState } from '../../context/AppStateContext';

export const AiCareCompanionScreen: React.FC = () => {
  const {
    aiRecommendations,
    completeAiRecommendation,
    addToast
  } = useAppState();

  return (
    <div className="p-4 space-y-4 pb-20">
      {/* Header */}
      <div>
        <h2 className="text-base font-bold text-slate-900">Care Companion Suggestions</h2>
        <p className="text-xs text-slate-500 font-medium">Personalized non-pharmacological care suggestions based on patient patterns</p>
      </div>

      {/* List of recommendations */}
      <div className="healthcare-section divide-y divide-slate-100">
        {aiRecommendations.map(rec => {
          const isCompleted = rec.status === 'completed';

          return (
            <div key={rec.id} className="p-4 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-teal-800 uppercase tracking-wider">{rec.activityType}</span>
                <span className="text-xs text-slate-500 font-medium">{rec.durationMinutes} mins · {rec.recommendedTime}</span>
              </div>

              <div>
                <h4 className="text-sm font-bold text-slate-900">{rec.title}</h4>
                <p className="text-xs text-slate-600 mt-1 leading-relaxed">
                  "{rec.reason}"
                </p>
              </div>

              <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
                {isCompleted ? (
                  <span className="text-xs font-bold text-emerald-700">✓ Activity completed</span>
                ) : (
                  <>
                    <button
                      onClick={() => addToast(`Marked "${rec.title}" as not suitable today.`, 'info')}
                      className="px-3 py-1.5 text-slate-500 hover:text-slate-800 text-xs font-semibold"
                    >
                      Not suitable
                    </button>
                    <button
                      onClick={() => addToast(`Started "${rec.title}" session.`, 'info')}
                      className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-semibold rounded-lg"
                    >
                      Start
                    </button>
                    <button
                      onClick={() => completeAiRecommendation(rec.id)}
                      className="px-3.5 py-1.5 bg-teal-700 hover:bg-teal-800 text-white text-xs font-semibold rounded-lg"
                    >
                      Completed
                    </button>
                  </>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Medical Disclaimer */}
      <p className="text-[11px] text-slate-400 text-center italic px-2">
        Care suggestions are supportive non-pharmacological recommendations and do not replace professional medical advice.
      </p>
    </div>
  );
};
