import React from 'react';

export const SkeletonCard: React.FC = () => (
  <div className="healthcare-card p-5 animate-pulse space-y-3">
    <div className="h-4 bg-slate-200 rounded-md w-1/3" />
    <div className="h-8 bg-slate-100 rounded-lg w-full" />
    <div className="flex justify-between items-center pt-2">
      <div className="h-3 bg-slate-200 rounded-md w-1/4" />
      <div className="h-3 bg-slate-200 rounded-md w-1/5" />
    </div>
  </div>
);

export const SkeletonTimeline: React.FC = () => (
  <div className="space-y-4 p-4 animate-pulse">
    {[1, 2, 3].map(i => (
      <div key={i} className="flex gap-4 items-start">
        <div className="w-10 h-10 bg-slate-200 rounded-full shrink-0" />
        <div className="flex-1 space-y-2">
          <div className="h-4 bg-slate-200 rounded-md w-1/2" />
          <div className="h-3 bg-slate-100 rounded-md w-3/4" />
        </div>
      </div>
    ))}
  </div>
);
