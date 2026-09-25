import React, { useState } from 'react';
import { useAppState } from '../../context/AppStateContext';
import type { CareReport } from '../../types';

export const ReportsScreen: React.FC = () => {
  const { reports, patient, addToast } = useAppState();
  const [previewReport, setPreviewReport] = useState<CareReport | null>(null);

  const reportCards = [
    { title: 'Weekly Care Summary', type: 'weekly', period: '15 Sep - 21 Sep 2026', size: '1.4 MB' },
    { title: 'Monthly Physician Briefing', type: 'doctor', period: 'August 2026', size: '2.1 MB' },
    { title: 'Medication Audit Report', type: 'medication', period: 'Last 30 Days', size: '890 KB' },
    { title: 'Cognitive & Habilitation Log', type: 'activity', period: 'Last 30 Days', size: '1.2 MB' },
    { title: 'Geofence & Safety Incident Log', type: 'safety', period: 'September 2026', size: '650 KB' }
  ];

  return (
    <div className="p-4 space-y-4 pb-20">
      {/* Header */}
      <div>
        <h2 className="text-base font-bold text-slate-900">Clinical & Care Reports</h2>
        <p className="text-xs text-slate-500 font-medium">Generate, preview and download physician briefings</p>
      </div>

      {/* List of Reports */}
      <div className="healthcare-section divide-y divide-slate-100">
        {reportCards.map(rep => {
          const matchedReport = reports.find(r => r.type === rep.type) || {
            id: 'rep-' + rep.type,
            title: rep.title,
            type: rep.type as CareReport['type'],
            generatedDate: '24 Sep 2026',
            period: rep.period,
            summary: `Automated care summary for ${patient.name} covering medication adherence, cognitive routines, and safety incidents.`,
            adherenceRate: 88,
            medicationRate: 91,
            cognitiveRate: 85,
            fileSize: rep.size
          };

          return (
            <div key={rep.type} className="p-4 space-y-2">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-bold text-slate-900">{rep.title}</h3>
                <span className="text-[11px] text-slate-400">{rep.size}</span>
              </div>
              <p className="text-xs text-slate-500 font-medium">Period: {rep.period}</p>

              <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
                <button
                  onClick={() => addToast(`Generated latest ${rep.title}`, 'success')}
                  className="px-3 py-1.5 text-xs font-semibold text-sky-700 hover:bg-sky-50 rounded-lg"
                >
                  Generate
                </button>
                <button
                  onClick={() => setPreviewReport(matchedReport)}
                  className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-lg"
                >
                  Preview
                </button>
                <button
                  onClick={() => addToast(`Downloading ${rep.title} PDF`, 'success')}
                  className="px-3.5 py-1.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold rounded-lg"
                >
                  Download
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* Practical Medical Report Preview Modal */}
      {previewReport && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl max-w-md w-full p-5 space-y-4 border border-slate-200 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-200 pb-3">
              <div>
                <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider">Clinical Report Brief</h3>
                <p className="text-xs text-slate-500">{previewReport.title}</p>
              </div>
              <button
                onClick={() => setPreviewReport(null)}
                className="text-slate-400 hover:text-slate-700 text-xs font-bold"
              >
                Close
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div className="flex justify-between pb-2 border-b border-slate-100">
                <div>
                  <span className="text-[10px] text-slate-400 font-bold uppercase">Patient</span>
                  <p className="font-bold text-slate-900">{patient.name} ({patient.age} yrs)</p>
                </div>
                <div className="text-right">
                  <span className="text-[10px] text-slate-400 font-bold uppercase">Physician</span>
                  <p className="font-bold text-slate-900">{patient.doctorName}</p>
                </div>
              </div>

              <div>
                <span className="font-bold text-slate-800 block mb-1">Executive Summary</span>
                <p className="text-slate-600 bg-slate-50 p-3 rounded-lg border border-slate-200 leading-relaxed">
                  {previewReport.summary}
                </p>
              </div>

              <div>
                <span className="font-bold text-slate-800 block mb-1">Metrics</span>
                <div className="grid grid-cols-3 gap-2 text-center">
                  <div className="bg-slate-50 p-2 rounded-lg border border-slate-200">
                    <span className="text-[10px] text-slate-500 block">Care</span>
                    <span className="font-bold text-slate-900">{previewReport.adherenceRate}%</span>
                  </div>
                  <div className="bg-slate-50 p-2 rounded-lg border border-slate-200">
                    <span className="text-[10px] text-slate-500 block">Medication</span>
                    <span className="font-bold text-slate-900">{previewReport.medicationRate}%</span>
                  </div>
                  <div className="bg-slate-50 p-2 rounded-lg border border-slate-200">
                    <span className="text-[10px] text-slate-500 block">Cognitive</span>
                    <span className="font-bold text-slate-900">{previewReport.cognitiveRate}%</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-200">
              <button
                onClick={() => setPreviewReport(null)}
                className="px-3.5 py-1.5 bg-slate-900 text-white font-semibold text-xs rounded-lg"
              >
                Done
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
