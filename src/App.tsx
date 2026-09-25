import React from 'react';
import { AppStateProvider, useAppState } from './context/AppStateContext';
import { PatientHeader } from './components/common/PatientHeader';
import { BottomNavigation } from './components/common/BottomNavigation';
import { ToastContainer } from './components/common/ToastContainer';
import { FloatingDemoControlBar } from './components/simulation/FloatingDemoControlBar';

import { HomeScreen } from './components/home/HomeScreen';
import { CareScreen } from './components/care/CareScreen';
import { MedicationScreen } from './components/medication/MedicationScreen';
import { MonitorScreen } from './components/monitor/MonitorScreen';
import { InsightsScreen } from './components/insights/InsightsScreen';
import { AiCareCompanionScreen } from './components/ai/AiCareCompanionScreen';
import { PatientTimelineScreen } from './components/timeline/PatientTimelineScreen';
import { ReportsScreen } from './components/reports/ReportsScreen';
import { MoreScreen } from './components/settings/MoreScreen';
import { Smartphone, Monitor as MonitorIcon } from 'lucide-react';

const AppContent: React.FC = () => {
  const { activeTab, isPhoneFrame, setIsPhoneFrame } = useAppState();

  const renderActiveTab = () => {
    switch (activeTab) {
      case 'home':
        return <HomeScreen />;
      case 'care':
        return <CareScreen />;
      case 'medication':
        return <MedicationScreen />;
      case 'monitor':
        return <MonitorScreen />;
      case 'insights':
        return <InsightsScreen />;
      case 'ai-companion':
        return <AiCareCompanionScreen />;
      case 'timeline':
        return <PatientTimelineScreen />;
      case 'reports':
        return <ReportsScreen />;
      case 'more':
        return <MoreScreen />;
      default:
        return <HomeScreen />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col items-center justify-center p-0 sm:p-4 font-sans antialiased text-slate-900">
      {/* Desktop View Switcher */}
      <div className="hidden sm:flex items-center justify-between w-full max-w-md mb-2 px-1 text-slate-500 text-xs">
        <span className="font-semibold text-slate-700">CareCompanion Mobile</span>

        <button
          onClick={() => setIsPhoneFrame(prev => !prev)}
          className="flex items-center gap-1.5 bg-white hover:bg-slate-50 text-slate-700 px-3 py-1 rounded-md border border-slate-300 shadow-xs transition-colors"
        >
          {isPhoneFrame ? (
            <>
              <MonitorIcon size={14} />
              <span>Full Container</span>
            </>
          ) : (
            <>
              <Smartphone size={14} />
              <span>390 × 844 Phone View</span>
            </>
          )}
        </button>
      </div>

      {/* Main Application Shell */}
      <div
        className={`w-full bg-slate-50 relative flex flex-col transition-all duration-200 ${
          isPhoneFrame
            ? 'phone-shell'
            : 'max-w-md min-h-screen sm:min-h-[844px] sm:rounded-2xl sm:border sm:border-slate-300 sm:shadow-lg overflow-hidden'
        }`}
      >
        {/* Mobile Notch Bar when in Phone View */}
        {isPhoneFrame && (
          <div className="w-full bg-slate-900 text-white text-[10px] px-6 pt-2 pb-1 flex justify-between items-center shrink-0 z-50">
            <span className="font-bold">9:41</span>
            <div className="w-20 h-3.5 bg-slate-950 rounded-full" />
            <span>5G</span>
          </div>
        )}

        {/* Quiet Patient Header */}
        <PatientHeader />

        {/* Dynamic Screen View */}
        <main className="flex-1 overflow-y-auto relative no-scrollbar">
          {renderActiveTab()}
        </main>

        {/* Sticky Mobile Bottom Navigation */}
        <BottomNavigation />
      </div>

      {/* Toast Notification Layer */}
      <ToastContainer />

      {/* Interactive Hackathon Simulation Bar */}
      <FloatingDemoControlBar />
    </div>
  );
};

export default function App() {
  return (
    <AppStateProvider>
      <AppContent />
    </AppStateProvider>
  );
}
