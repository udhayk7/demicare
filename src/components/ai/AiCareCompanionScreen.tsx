import React, { useState } from 'react';
import { useAppState } from '../../context/AppStateContext';
import { ChevronDown, ChevronUp, Sparkles, CheckCircle2 } from 'lucide-react';

export const AiCareCompanionScreen: React.FC = () => {
  const {
    aiRecommendations,
    completeAiRecommendation,
    addToast
  } = useAppState();

  const [expandedRecId, setExpandedRecId] = useState<string | null>(aiRecommendations[0]?.id || null);
  const [feedbackRecId, setFeedbackRecId] = useState<string | null>(null);
  const [selectedResponse, setSelectedResponse] = useState<string>('enjoyed');

  const feedbackOptions = [
    { id: 'enjoyed', label: 'Enjoyed it', emoji: '😊' },
    { id: 'neutral', label: 'Stayed neutral', emoji: '😐' },
    { id: 'disliked', label: 'Disliked it', emoji: '🙁' },
    { id: 'tired', label: 'Became tired', emoji: '🥱' },
    { id: 'assistance_needed', label: 'Needed assistance', emoji: '🤝' },
    { id: 'refused', label: 'Refused', emoji: '✋' }
  ];

  const handleSaveFeedback = (recId: string) => {
    completeAiRecommendation(recId, selectedResponse);
    setFeedbackRecId(null);
  };

  return (
    <div className="p-4 space-y-4 pb-20">
      {/* Header */}
      <div>
        <h2 className="text-base font-bold text-slate-900">Care Companion Suggestions</h2>
        <p className="text-xs text-slate-500 font-medium">Personalized non-pharmacological care suggestions based on patient patterns</p>
      </div>

      {/* Longitudinal Care Intelligence Evidence Strip (Sections 4 & 5) */}
      <div className="bg-teal-50/80 border border-teal-200 rounded-xl p-3.5 text-xs space-y-1.5 shadow-xs">
        <div className="flex items-center justify-between">
          <span className="font-bold text-teal-950 flex items-center gap-1.5">
            <Sparkles size={14} className="text-teal-700" />
            <span>Care Pattern Intelligence</span>
          </span>
          <span className="text-[10px] bg-teal-100 text-teal-800 px-2 py-0.5 rounded-full font-bold">
            Data → Activity Loop
          </span>
        </div>
        <p className="text-[11px] text-teal-900/90 leading-relaxed">
          Correlating recorded care observations (sleep 6.1h avg, evening restlessness, lower hydration) with Raghavan's personalized hobbies (Carnatic music & reminiscence).
        </p>
      </div>

      {/* List of recommendations */}
      <div className="healthcare-section divide-y divide-slate-100">
        {aiRecommendations.map(rec => {
          const isCompleted = rec.status === 'completed';
          const isExpanded = expandedRecId === rec.id;

          return (
            <div key={rec.id} className="p-4 space-y-3">
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

              {/* Expandable Structured Clinical Breakdown */}
              <div className="pt-1">
                <button
                  onClick={() => setExpandedRecId(isExpanded ? null : rec.id)}
                  className="flex items-center gap-1 text-[11px] font-semibold text-teal-700 hover:text-teal-900"
                >
                  <span>{isExpanded ? 'Hide clinical rationale' : 'View clinical rationale & evidence'}</span>
                  {isExpanded ? <ChevronUp size={13} /> : <ChevronDown size={13} />}
                </button>

                {isExpanded && (
                  <div className="mt-2.5 p-3 bg-teal-50/50 rounded-lg border border-teal-100 text-xs space-y-2">
                    {rec.observed && (
                      <div>
                        <span className="font-bold text-slate-800 uppercase tracking-wider text-[10px] block">Observed Pattern</span>
                        <p className="text-slate-600 text-xs mt-0.5">{rec.observed}</p>
                      </div>
                    )}
                    {rec.whyItMatters && (
                      <div>
                        <span className="font-bold text-slate-800 uppercase tracking-wider text-[10px] block">Why It Matters</span>
                        <p className="text-slate-600 text-xs mt-0.5">{rec.whyItMatters}</p>
                      </div>
                    )}
                    {rec.suggestedAction && (
                      <div>
                        <span className="font-bold text-slate-800 uppercase tracking-wider text-[10px] block">Suggested Non-Pharmacological Action</span>
                        <p className="text-slate-600 text-xs mt-0.5">{rec.suggestedAction}</p>
                      </div>
                    )}
                    {rec.whyThisActivity && (
                      <div>
                        <span className="font-bold text-slate-800 uppercase tracking-wider text-[10px] block">Personalization (Patient Preferences)</span>
                        <p className="text-slate-600 text-xs mt-0.5">{rec.whyThisActivity}</p>
                      </div>
                    )}
                    {rec.safetyCarePlan && (
                      <div>
                        <span className="font-bold text-slate-800 uppercase tracking-wider text-[10px] block">Care Plan & Safety Boundary</span>
                        <p className="text-slate-600 text-xs mt-0.5">{rec.safetyCarePlan}</p>
                      </div>
                    )}
                    {rec.expectedOutcome && (
                      <div>
                        <span className="font-bold text-slate-800 uppercase tracking-wider text-[10px] block">Expected Observation</span>
                        <p className="text-slate-600 text-xs mt-0.5">{rec.expectedOutcome}</p>
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* Action Buttons */}
              <div className="flex items-center justify-between pt-2 border-t border-slate-100">
                {isCompleted ? (
                  <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-700">
                    <CheckCircle2 size={14} />
                    <span>Activity completed · Outcome: {rec.caregiverFeedback || 'Enjoyed it'}</span>
                  </div>
                ) : (
                  <>
                    <button
                      onClick={() => addToast(`Marked "${rec.title}" as not suitable today.`, 'info')}
                      className="px-2.5 py-1.5 text-slate-500 hover:text-slate-800 text-xs font-semibold"
                    >
                      Not suitable
                    </button>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => addToast(`Started "${rec.title}" session.`, 'info')}
                        className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-semibold rounded-lg"
                      >
                        Start
                      </button>
                      <button
                        onClick={() => setFeedbackRecId(rec.id)}
                        className="px-3.5 py-1.5 bg-teal-700 hover:bg-teal-800 text-white text-xs font-semibold rounded-lg shadow-xs flex items-center gap-1"
                      >
                        <Sparkles size={12} />
                        <span>Complete & Record</span>
                      </button>
                    </div>
                  </>
                )}
              </div>

              {/* Interactive Caregiver Feedback Dialog */}
              {feedbackRecId === rec.id && (
                <div className="mt-3 p-3.5 bg-white border border-teal-300 rounded-xl shadow-md space-y-3">
                  <div className="flex items-center justify-between">
                    <h5 className="text-xs font-bold text-slate-900">Record Patient Response</h5>
                    <span className="text-[10px] text-teal-700 font-semibold uppercase">Feedback Loop</span>
                  </div>
                  <p className="text-[11px] text-slate-600">
                    How did Raghavan respond to this activity? Your feedback personalizes future recommendations.
                  </p>

                  <div className="grid grid-cols-2 gap-1.5 text-xs">
                    {feedbackOptions.map(opt => (
                      <button
                        key={opt.id}
                        type="button"
                        onClick={() => setSelectedResponse(opt.id)}
                        className={`p-2 rounded-lg text-left font-medium border flex items-center gap-2 transition-all ${
                          selectedResponse === opt.id
                            ? 'bg-teal-50 border-teal-500 text-teal-900 font-bold ring-1 ring-teal-500'
                            : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-50'
                        }`}
                      >
                        <span>{opt.emoji}</span>
                        <span>{opt.label}</span>
                      </button>
                    ))}
                  </div>

                  <div className="flex items-center justify-end gap-2 pt-1">
                    <button
                      onClick={() => setFeedbackRecId(null)}
                      className="px-3 py-1.5 text-xs font-semibold text-slate-500 hover:bg-slate-100 rounded-lg"
                    >
                      Cancel
                    </button>
                    <button
                      onClick={() => handleSaveFeedback(rec.id)}
                      className="px-3.5 py-1.5 text-xs font-semibold bg-teal-700 hover:bg-teal-800 text-white rounded-lg"
                    >
                      Save Outcome
                    </button>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Clinical Safety Boundary (Section 7) */}
      <div className="bg-slate-100/80 border border-slate-200 rounded-xl p-3 text-[11px] text-slate-600 text-center space-y-0.5">
        <span className="font-bold text-slate-800 uppercase tracking-wider text-[10px] block">
          Clinical Safety Boundary
        </span>
        <p className="leading-relaxed">
          Non-pharmacological caregiver guidance only. The system does not diagnose, prescribe, or alter physician care plans.
        </p>
      </div>
    </div>
  );
};

