import React from 'react';
import type { PatientStatus, MedicationStatus } from '../../types';

interface StatusBadgeProps {
  status: PatientStatus | MedicationStatus | 'connected' | 'disconnected' | 'at_home' | 'safe_zone_exit' | 'wandering' | 'info' | string;
  label?: string;
  size?: 'sm' | 'md';
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, label, size = 'md' }) => {
  let dotColor = 'bg-slate-400';
  let textColor = 'text-slate-700';
  let text = label || status;

  switch (status) {
    case 'stable':
    case 'taken':
    case 'connected':
    case 'at_home':
    case 'completed':
    case 'resolved':
      dotColor = 'bg-emerald-500';
      textColor = 'text-emerald-800 font-semibold';
      if (!label) {
        text = status === 'stable' ? 'Stable' : status === 'taken' ? 'Taken' : status === 'connected' ? 'Connected' : status === 'at_home' ? 'At home' : 'Completed';
      }
      break;

    case 'attention':
    case 'pending':
    case 'snoozed':
    case 'low_battery':
      dotColor = 'bg-amber-500';
      textColor = 'text-amber-800 font-semibold';
      if (!label) {
        text = status === 'attention' ? 'Attention required' : status === 'pending' ? 'Pending' : 'Pending';
      }
      break;

    case 'critical':
    case 'missed':
    case 'disconnected':
    case 'safe_zone_exit':
    case 'wandering':
    case 'sos':
      dotColor = 'bg-rose-600';
      textColor = 'text-rose-700 font-bold';
      if (!label) {
        text = status === 'critical' ? 'Critical alert' : status === 'missed' ? 'Missed' : status === 'safe_zone_exit' ? 'Safe zone exit' : 'Disconnected';
      }
      break;

    case 'info':
    default:
      dotColor = 'bg-sky-500';
      textColor = 'text-slate-700 font-medium';
      if (!label) text = 'Information';
      break;
  }

  const textSize = size === 'sm' ? 'text-[11px]' : 'text-xs';

  return (
    <span className={`inline-flex items-center gap-1.5 ${textSize} ${textColor}`}>
      <span className={`w-2 h-2 rounded-full ${dotColor} shrink-0`} />
      <span className="capitalize">{text}</span>
    </span>
  );
};
