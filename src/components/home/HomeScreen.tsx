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
    <div className="w-full max-w-5xl mx-auto p-4 sm:p-6 lg:p-8 space-y-4 md:space-y-6 pb-[calc(5.5rem+env(safe-area-inset-bottom,0px))] md:pb-12">
      {/* Attention Card (Shown if attention needed or pending items) */}
      {patient.status !== 'stable' && <AttentionCard />}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 md:gap-6 items-start">
        {/* Left Column */}
        <div className="space-y-4 md:space-y-6">
          <CareOverviewCard />
          <NextUpCard />
          <AiCompanionCard />
        </div>

        {/* Right Column */}
        <div className="space-y-4 md:space-y-6">
          <PatientStatusCard />
          <QuickActionsGrid />
        </div>
      </div>
    </div>
  );
};
