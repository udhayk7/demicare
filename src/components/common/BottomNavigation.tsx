import React from 'react';
import { Home, Heart, Shield, BarChart2, MoreHorizontal } from 'lucide-react';
import { useAppState } from '../../context/AppStateContext';
import type { NavigationTab } from '../../types';

export const BottomNavigation: React.FC = () => {
  const { activeTab, setActiveTab, patient } = useAppState();

  const navItems: { id: NavigationTab; label: string; icon: React.ElementType; badge?: boolean }[] = [
    { id: 'home', label: 'Home', icon: Home, badge: patient.status !== 'stable' },
    { id: 'care', label: 'Care', icon: Heart },
    { id: 'monitor', label: 'Monitor', icon: Shield },
    { id: 'insights', label: 'Insights', icon: BarChart2 },
    { id: 'more', label: 'More', icon: MoreHorizontal }
  ];

  return (
    <nav
      className="fixed bottom-0 left-0 right-0 z-40 bg-white/95 backdrop-blur-sm border-t border-slate-200 md:hidden shadow-[0_-2px_12px_rgba(0,0,0,0.04)]"
      style={{ paddingBottom: 'max(0.35rem, env(safe-area-inset-bottom, 0px))' }}
    >
      <div className="flex items-center justify-around w-full max-w-lg mx-auto px-2 pt-1.5 pb-1">
        {navItems.map(item => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`flex flex-col items-center justify-center py-1 px-3 transition-colors relative ${
                isActive ? 'text-sky-700 font-bold' : 'text-slate-500 hover:text-slate-800 font-medium'
              }`}
            >
              <div className="relative">
                <Icon size={20} strokeWidth={isActive ? 2.2 : 1.7} />
                {item.badge && !isActive && (
                  <span className="absolute -top-1 -right-1 w-2 h-2 bg-amber-500 rounded-full" />
                )}
              </div>
              <span className="text-[11px] mt-1 tracking-tight">{item.label}</span>
            </button>
          );
        })}
      </div>
    </nav>
  );
};
