import React, { useState } from 'react';
import { useAppState } from '../../context/AppStateContext';
import type { EventCategory } from '../../types';

export const PatientTimelineScreen: React.FC = () => {
  const { timelineEvents } = useAppState();
  const [selectedCategory, setSelectedCategory] = useState<EventCategory>('all');

  const categories: { id: EventCategory; label: string }[] = [
    { id: 'all', label: 'All' },
    { id: 'medication', label: 'Medication' },
    { id: 'activities', label: 'Activities' },
    { id: 'behaviour', label: 'Behaviour' },
    { id: 'safety', label: 'Safety' },
    { id: 'location', label: 'Location' },
    { id: 'camera', label: 'Camera' }
  ];

  const filteredEvents = selectedCategory === 'all'
    ? timelineEvents
    : timelineEvents.filter(e => e.category === selectedCategory);

  return (
    <div className="w-full max-w-4xl mx-auto p-4 sm:p-6 lg:p-8 space-y-4 md:space-y-6 pb-[calc(5.5rem+env(safe-area-inset-bottom,0px))] md:pb-12">
      {/* Header */}
      <div>
        <h2 className="text-base font-bold text-slate-900">Activity & Timeline</h2>
        <p className="text-xs text-slate-500 font-medium">Unified longitudinal care memory · Single source of truth</p>
      </div>

      {/* Category filter pills */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1 no-scrollbar">
        {categories.map(cat => {
          const isSelected = selectedCategory === cat.id;
          return (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              className={`px-3 py-1 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors ${
                isSelected
                  ? 'bg-slate-900 text-white'
                  : 'bg-white text-slate-600 hover:bg-slate-100 border border-slate-200'
              }`}
            >
              {cat.label}
            </button>
          );
        })}
      </div>

      {/* Clean list rows with thin horizontal dividers */}
      <div className="healthcare-section divide-y divide-slate-100">
        {filteredEvents.length === 0 ? (
          <div className="text-center text-xs text-slate-400 py-8">
            No events found for "{selectedCategory}".
          </div>
        ) : (
          filteredEvents.map(event => {
            const isAlert = event.severity === 'alert';
            const isWarning = event.severity === 'warning';
            const isSuccess = event.severity === 'success';

            return (
              <div key={event.id} className="p-3.5 space-y-1">
                <div className="flex items-center justify-between text-xs">
                  <div className="flex items-center gap-1.5 flex-wrap">
                    <span
                      className={`w-2 h-2 rounded-full shrink-0 ${
                        isAlert
                          ? 'bg-rose-600'
                          : isWarning
                          ? 'bg-amber-500'
                          : isSuccess
                          ? 'bg-emerald-500'
                          : 'bg-sky-500'
                      }`}
                    />
                    <span className="font-bold text-slate-900">{event.title}</span>
                    <span className="text-[9px] px-1.5 py-0.2 rounded bg-slate-100 text-slate-500 font-semibold uppercase tracking-wider">
                      {event.category}
                    </span>
                  </div>
                  <span className="text-[11px] text-slate-400 font-medium shrink-0">{event.timeDisplay}</span>
                </div>

                <p className="text-xs text-slate-600 pl-3.5 leading-relaxed">{event.description}</p>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
