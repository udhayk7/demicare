import React from 'react';
import { CareOverviewCard } from './CareOverviewCard';
import { AttentionCard } from './AttentionCard';
import { NextUpCard } from './NextUpCard';
import { PatientStatusCard } from './PatientStatusCard';
import { AiCompanionCard } from './AiCompanionCard';
import { QuickActionsGrid } from './QuickActionsGrid';
import { useAppState } from '../../context/AppStateContext';

export const HomeScreen: React.FC = () => {
  const { patient } = useAppState();

  return (
    <div className="p-4 space-y-4 pb-20">
      {/* 1. Care Overview Progress Card */}
      <CareOverviewCard />

      {/* 2. Attention Card (Shown if attention needed or pending items) */}
      {patient.status !== 'stable' && <AttentionCard />}

      {/* 3. Next Up Medication / Event Card */}
      <NextUpCard />

      {/* 4. Real-Time Patient Status Monitoring Card */}
      <PatientStatusCard />

      {/* 5. AI Care Companion Suggestion Card */}
      <AiCompanionCard />

      {/* 6. Quick Actions Grid */}
      <QuickActionsGrid />
    </div>
  );
};
