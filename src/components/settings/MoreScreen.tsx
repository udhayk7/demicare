import React from 'react';
import { useAppState } from '../../context/AppStateContext';

export const MoreScreen: React.FC = () => {
  const { patient, addToast, setActiveTab } = useAppState();

  const sections = [
    {
      title: 'Patient Profile & Medical',
      items: [
        { label: 'Patient Profile & History', action: () => addToast('Viewing Raghavan Menon profile', 'info') },
        { label: 'Medical Documents & Prescriptions', action: () => setActiveTab('reports') },
        { label: 'Care Team & Physician Contacts', action: () => addToast('Care Team: Dr. Arun Nair, Anu Menon, Suresh Menon', 'info') }
      ]
    },
    {
      title: 'Connected Devices',
      items: [
        { label: 'Pendant Diagnostics & Battery', action: () => setActiveTab('monitor') },
        { label: 'Geofence & Alert Sensitivity Settings', action: () => addToast('Safe Zone Radius set to 150 meters', 'info') }
      ]
    },
    {
      title: 'Account & Privacy',
      items: [
        { label: 'Caregiver Account (Anu Menon)', action: () => addToast('Caregiver: Anu Menon (Daughter)', 'info') },
        { label: 'Notifications & Alerts', action: () => addToast('Alerts enabled via SMS & Push', 'info') },
        { label: 'Privacy & Data Protection', action: () => addToast('End-to-end encrypted logs', 'info') }
      ]
    },
    {
      title: 'App & Support',
      items: [
        { label: 'Caregiver Helpline', action: () => addToast('24/7 Helpline: 1800-425-CARE', 'info') },
        { label: 'About CareCompanion v1.0', action: () => addToast('CareCompanion Hackathon Edition', 'info') },
        { label: 'Sign Out Session', action: () => addToast('Session locked safely.', 'info'), danger: true }
      ]
    }
  ];

  return (
    <div className="p-4 space-y-4 pb-20">
      {/* Header */}
      <div>
        <h2 className="text-base font-bold text-slate-900">Settings & Account</h2>
        <p className="text-xs text-slate-500 font-medium">Care team, patient profile, device parameters & app options</p>
      </div>

      {/* Patient info row */}
      <div className="healthcare-section p-4 flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-slate-900">{patient.name}</h3>
          <p className="text-xs text-slate-500">{patient.age} yrs · {patient.condition}</p>
        </div>
        <span className="text-xs font-semibold text-emerald-700">● Care Active</span>
      </div>

      {/* Settings groups */}
      {sections.map(sec => (
        <div key={sec.title} className="space-y-1.5">
          <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider">{sec.title}</h3>
          <div className="healthcare-section divide-y divide-slate-100">
            {sec.items.map(item => (
              <button
                key={item.label}
                onClick={item.action}
                className={`w-full p-3.5 text-left text-xs font-semibold flex items-center justify-between hover:bg-slate-50 transition-colors ${
                  item.danger ? 'text-rose-600' : 'text-slate-800'
                }`}
              >
                <span>{item.label}</span>
                <span className="text-slate-400 font-normal text-sm">›</span>
              </button>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};
