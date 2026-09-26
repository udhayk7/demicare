import React from 'react';
import {
  Home,
  Heart,
  Pill,
  Shield,
  Sparkles,
  BarChart2,
  Clock,
  FileText,
  Settings,
  HeartPulse
} from 'lucide-react';
import { useAppState } from '../../context/AppStateContext';
import { StatusBadge } from './StatusBadge';
import type { NavigationTab } from '../../types';

export const DesktopSidebar: React.FC = () => {
  const { activeTab, setActiveTab, patient } = useAppState();

  const navItems: { id: NavigationTab; label: string; icon: React.ElementType; badge?: string }[] = [
    { id: 'home', label: 'Dashboard', icon: Home },
    { id: 'care', label: 'Care Plan & Routines', icon: Heart },
    { id: 'medication', label: 'Medications', icon: Pill },
    { id: 'monitor', label: 'Monitor & Safety', icon: Shield, badge: patient.status !== 'stable' ? 'Alert' : undefined },
    { id: 'ai-companion', label: 'AI Care Companion', icon: Sparkles, badge: 'Active' },
    { id: 'insights', label: 'Insights & Patterns', icon: BarChart2 },
    { id: 'timeline', label: 'Patient Timeline', icon: Clock },
    { id: 'reports', label: 'Physician Reports', icon: FileText },
    { id: 'more', label: 'Settings & Account', icon: Settings },
  ];

  return (
    <aside className="hidden md:flex flex-col w-64 lg:w-72 bg-white border-r border-slate-200 shrink-0 h-screen sticky top-0 z-30">
      {/* Brand & Logo Header */}
      <div className="p-5 border-b border-slate-200 flex items-center gap-3">
        <div className="w-9 h-9 rounded-xl bg-sky-700 text-white flex items-center justify-center shadow-xs">
          <HeartPulse size={20} />
        </div>
        <div>
          <h1 className="text-sm font-bold text-slate-900 tracking-tight leading-none">
            CareCompanion
          </h1>
          <p className="text-[11px] text-slate-500 font-medium mt-1">
            Dementia Care Platform
          </p>
        </div>
      </div>

      {/* Patient Profile Card Brief */}
      <div className="p-4 border-b border-slate-100 bg-slate-50/70">
        <div className="flex items-center gap-3">
          <img
            src={patient.avatarUrl}
            alt={patient.name}
            className="w-10 h-10 rounded-full object-cover border border-slate-200 shadow-xs"
          />
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-1.5">
              <span className="font-bold text-slate-900 text-xs truncate">{patient.name}</span>
              <StatusBadge status={patient.status} size="sm" />
            </div>
            <p className="text-[11px] text-slate-500 truncate mt-0.5">
              {patient.stage} · {patient.age}y
            </p>
          </div>
        </div>
      </div>

      {/* Navigation List */}
      <nav className="flex-1 overflow-y-auto p-3 space-y-1 no-scrollbar">
        <div className="text-[10px] font-bold uppercase tracking-wider text-slate-400 px-3 py-1.5">
          Caregiver Navigation
        </div>
        {navItems.map(item => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-xs font-semibold transition-all ${
                isActive
                  ? 'bg-sky-50 text-sky-800 font-bold border border-sky-200 shadow-2xs'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/80 border border-transparent'
              }`}
            >
              <div className="flex items-center gap-2.5">
                <Icon
                  size={16}
                  className={isActive ? 'text-sky-700' : 'text-slate-400'}
                  strokeWidth={isActive ? 2.2 : 1.8}
                />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span
                  className={`text-[10px] px-1.5 py-0.5 rounded-full font-bold uppercase tracking-wide ${
                    item.badge === 'Alert'
                      ? 'bg-rose-100 text-rose-700'
                      : 'bg-teal-100 text-teal-800'
                  }`}
                >
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Footer Caregiver Indicator */}
      <div className="p-3.5 border-t border-slate-200 bg-slate-50 text-[11px] text-slate-500 flex items-center justify-between">
        <div>
          <span className="font-semibold text-slate-700 block">Caregiver Active</span>
          <span className="text-[10px] text-slate-400">{patient.primaryCaregiver}</span>
        </div>
        <span className="w-2 h-2 rounded-full bg-emerald-500" title="Online" />
      </div>
    </aside>
  );
};
