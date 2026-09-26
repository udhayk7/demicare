import React from 'react';
import { AppStateProvider, useAppState } from './context/AppStateContext';
import { PatientHeader } from './components/common/PatientHeader';
import { DesktopSidebar } from './components/common/DesktopSidebar';
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

const AppContent: React.FC = () => {
  const { activeTab } = useAppState();

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
    <div className="w-full min-h-[100dvh] flex flex-col md:flex-row bg-slate-100 font-sans antialiased text-slate-900 overflow-x-hidden">
      {/* Desktop Responsive Navigation Sidebar (hidden on mobile, visible on desktop/laptop) */}
      <DesktopSidebar />

      {/* Main Responsive Application Workspace */}
      <div className="flex-1 flex flex-col min-w-0 min-h-[100dvh] bg-slate-50 relative">
        {/* Top Header */}
        <PatientHeader />

        {/* Dynamic Screen View - scrolls naturally with full viewport width */}
        <main className="flex-1 overflow-y-auto relative w-full">
          {renderActiveTab()}
        </main>

        {/* Fixed Mobile Bottom Navigation (fixed to bottom of viewport, hidden on desktop) */}
        <BottomNavigation />
      </div>

      {/* Toast Notification Layer */}
      <ToastContainer />

      {/* Developer Simulation Bar (Hidden by default in normal/judge presentation UI) */}
      {import.meta.env.VITE_SHOW_SIMULATOR === 'true' && <FloatingDemoControlBar />}
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
