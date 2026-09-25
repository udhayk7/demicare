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
    <nav className="bg-white border-t border-slate-200 sticky bottom-0 z-40 px-2 py-1.5">
      <div className="flex items-center justify-around max-w-md mx-auto">
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
