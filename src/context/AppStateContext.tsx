import React, { createContext, useContext, useState } from 'react';
import type {
  Patient,
  Medication,
  RoutineItem,
  HabilitationActivity,
  CognitiveActivity,
  BehaviourObservation,
  Appointment,
  LocationData,
  MovementData,
  SleepData,
  SafetyEvent,
  FamiliarPerson,
  RecognitionEvent,
  PendantStatus,
  AIRecommendation,
  AIInsight,
  TimelineEvent,
  CareReport,
  NotificationItem,
  NavigationTab
} from '../types';
import {
  initialPatient,
  initialMedications,
  initialRoutines,
  initialHabilitationActivities,
  initialCognitiveActivities,
  initialObservations,
  initialAppointments,
  initialLocation,
  initialMovement,
  initialSleep,
  initialSafetyEvents,
  initialFamiliarPeople,
  initialRecognitionEvents,
  initialPendant,
  initialAIRecommendations,
  initialAIInsights,
  initialTimelineEvents,
  initialReports,
  initialNotifications
} from '../data/mockData';

export interface Toast {
  id: string;
  message: string;
  type?: 'success' | 'warning' | 'alert' | 'info';
}

interface AppStateContextType {
  activeTab: NavigationTab;
  setActiveTab: (tab: NavigationTab) => void;
  isPhoneFrame: boolean;
  setIsPhoneFrame: (val: boolean | ((prev: boolean) => boolean)) => void;
  patient: Patient;
  medications: Medication[];
  routines: RoutineItem[];
  habilitation: HabilitationActivity[];
  cognitive: CognitiveActivity[];
  observations: BehaviourObservation[];
  appointments: Appointment[];
  location: LocationData;
  movement: MovementData;
  sleep: SleepData;
  safetyEvents: SafetyEvent[];
  pendant: PendantStatus;
  familiarPeople: FamiliarPerson[];
  recognitionEvents: RecognitionEvent[];
  aiRecommendations: AIRecommendation[];
  aiInsights: AIInsight[];
  timelineEvents: TimelineEvent[];
  reports: CareReport[];
  notifications: NotificationItem[];
  toasts: Toast[];

  // Actions & Simulation handlers
  addToast: (message: string, type?: Toast['type']) => void;
  removeToast: (id: string) => void;
  markMedicationTaken: (id: string) => void;
  markMedicationMissed: (id: string) => void;
  toggleHabilitation: (id: string) => void;
  toggleCognitive: (id: string) => void;
  logBehaviourObservation: (type: BehaviourObservation['type'], note: string, intensity?: BehaviourObservation['intensity']) => void;
  completeAiRecommendation: (id: string) => void;
  
  // Simulations
  simulateMedicationReminder: () => void;
  simulateSOS: () => void;
  simulateGeofenceExit: () => void;
  simulateReturnHome: () => void;
  simulatePersonDetected: (personName: string, relation: string) => void;
  simulateUnknownPersonDetected: () => void;
  simulateGenerateNewRecommendation: () => void;
  resetSimulations: () => void;
}

const AppStateContext = createContext<AppStateContextType | undefined>(undefined);

export const AppStateProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [activeTab, setActiveTab] = useState<NavigationTab>('home');
  const [isPhoneFrame, setIsPhoneFrame] = useState<boolean>(true);
  
  const [patient, setPatient] = useState<Patient>(initialPatient);
  const [medications, setMedications] = useState<Medication[]>(initialMedications);
  const [routines, setRoutines] = useState<RoutineItem[]>(initialRoutines);
  const [habilitation, setHabilitation] = useState<HabilitationActivity[]>(initialHabilitationActivities);
  const [cognitive, setCognitive] = useState<CognitiveActivity[]>(initialCognitiveActivities);
  const [observations, setObservations] = useState<BehaviourObservation[]>(initialObservations);
  const [appointments] = useState<Appointment[]>(initialAppointments);
  
  const [location, setLocation] = useState<LocationData>(initialLocation);
  const [movement] = useState<MovementData>(initialMovement);
  const [sleep] = useState<SleepData>(initialSleep);
  const [safetyEvents, setSafetyEvents] = useState<SafetyEvent[]>(initialSafetyEvents);
  const [pendant, setPendant] = useState<PendantStatus>(initialPendant);
  const [familiarPeople] = useState<FamiliarPerson[]>(initialFamiliarPeople);
  const [recognitionEvents, setRecognitionEvents] = useState<RecognitionEvent[]>(initialRecognitionEvents);
  
  const [aiRecommendations, setAiRecommendations] = useState<AIRecommendation[]>(initialAIRecommendations);
  const [aiInsights] = useState<AIInsight[]>(initialAIInsights);
  const [timelineEvents, setTimelineEvents] = useState<TimelineEvent[]>(initialTimelineEvents);
  const [reports] = useState<CareReport[]>(initialReports);
  const [notifications, setNotifications] = useState<NotificationItem[]>(initialNotifications);
  const [toasts, setToasts] = useState<Toast[]>([]);

  const addToast = (message: string, type: Toast['type'] = 'info') => {
    const id = 'toast-' + Date.now() + '-' + Math.random().toString(36).substr(2, 4);
    setToasts(prev => [...prev.slice(-4), { id, message, type }]);
    setTimeout(() => {
      removeToast(id);
    }, 3800);
  };

  const removeToast = (id: string) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  };

  const addTimelineEvent = (
    title: string,
    description: string,
    category: TimelineEvent['category'],
    severity: TimelineEvent['severity'] = 'info',
    iconName: string = 'Bell'
  ) => {
    const now = new Date();
    const timeDisplay = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const newEvent: TimelineEvent = {
      id: 'tl-' + Date.now(),
      timestamp: now.toISOString(),
      timeDisplay,
      title,
      description,
      category,
      severity,
      iconName
    };
    setTimelineEvents(prev => [newEvent, ...prev]);
  };

  const markMedicationTaken = (id: string) => {
    let medName = '';
    setMedications(prev =>
      prev.map(m => {
        if (m.id === id) {
          medName = m.name;
          return { ...m, status: 'taken' as const };
        }
        return m;
      })
    );
    // Update progress routine
    setRoutines(prev =>
      prev.map(r => (r.category === 'medication' ? { ...r, completed: Math.min(r.total, r.completed + 1) } : r))
    );
    addToast(`${medName || 'Medication'} marked as taken.`, 'success');
    addTimelineEvent('Medication Taken', `${medName} acknowledged by caregiver.`, 'medication', 'success', 'CheckCircle2');
  };

  const markMedicationMissed = (id: string) => {
    let medName = '';
    setMedications(prev =>
      prev.map(m => {
        if (m.id === id) {
          medName = m.name;
          return { ...m, status: 'missed' as const };
        }
        return m;
      })
    );
    addToast(`${medName || 'Medication'} marked as missed.`, 'warning');
    addTimelineEvent('Medication Missed', `${medName} scheduled dosage missed.`, 'medication', 'warning', 'AlertCircle');
  };

  const toggleHabilitation = (id: string) => {
    let title = '';
    let nowCompleted = false;
    setHabilitation(prev =>
      prev.map(h => {
        if (h.id === id) {
          title = h.title;
          nowCompleted = !h.completed;
          return { ...h, completed: nowCompleted };
        }
        return h;
      })
    );
    addToast(nowCompleted ? `Completed "${title}"` : `Reopened "${title}"`, 'info');
    if (nowCompleted) {
      addTimelineEvent('Activity Completed', `Completed: ${title}`, 'activities', 'success', 'Sparkles');
    }
  };

  const toggleCognitive = (id: string) => {
    let title = '';
    let nowCompleted = false;
    setCognitive(prev =>
      prev.map(c => {
        if (c.id === id) {
          title = c.title;
          nowCompleted = !c.completed;
          return { ...c, completed: nowCompleted };
        }
        return c;
      })
    );
    addToast(nowCompleted ? `Completed "${title}"` : `Reopened "${title}"`, 'info');
    if (nowCompleted) {
      addTimelineEvent('Cognitive Task Completed', `Finished task: ${title}`, 'activities', 'success', 'Brain');
    }
  };

  const logBehaviourObservation = (type: BehaviourObservation['type'], note: string, intensity: BehaviourObservation['intensity'] = 'mild') => {
    const timeDisplay = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const newObs: BehaviourObservation = {
      id: 'obs-' + Date.now(),
      timestamp: timeDisplay,
      type,
      note,
      intensity,
      caregiverActionTaken: 'Logged & observed by caregiver.'
    };
    setObservations(prev => [newObs, ...prev]);
    addToast(`Logged behaviour observation (${type})`, 'info');
    addTimelineEvent(`Behaviour Logged: ${type.toUpperCase()}`, note, 'behaviour', 'info', 'Eye');
  };

  const completeAiRecommendation = (id: string) => {
    let title = '';
    setAiRecommendations(prev =>
      prev.map(r => {
        if (r.id === id) {
          title = r.title;
          return { ...r, status: 'completed' as const };
        }
        return r;
      })
    );
    addToast(`AI Suggested Activity "${title}" completed!`, 'success');
    addTimelineEvent('AI Suggested Activity Completed', title, 'activities', 'success', 'Bot');
  };

  // --- DEMO SIMULATION METHODS ---

  const simulateMedicationReminder = () => {
    addToast('💊 Demo Simulation: Evening Medication Reminder Triggered', 'warning');
    setPatient(prev => ({ ...prev, status: 'attention' }));
    addTimelineEvent('Medication Alert', 'Donepezil 5mg (9:00 PM) reminder unacknowledged.', 'medication', 'warning', 'Pill');
    setNotifications(prev => [
      {
        id: 'notif-' + Date.now(),
        title: 'Medication Alert',
        message: 'Donepezil 5mg scheduled for 9:00 PM needs confirmation.',
        timestamp: 'Just now',
        read: false,
        type: 'medication'
      },
      ...prev
    ]);
  };

  const simulateSOS = () => {
    addToast('🚨 EMERGENCY SIMULATION: Pendant SOS Triggered!', 'alert');
    setPatient(prev => ({ ...prev, status: 'critical' }));
    setPendant(prev => ({ ...prev, batteryLevel: Math.max(10, prev.batteryLevel - 5) }));
    const newSafetyEvent: SafetyEvent = {
      id: 'safe-sos-' + Date.now(),
      timestamp: 'Just now',
      type: 'sos_button',
      severity: 'critical',
      resolved: false,
      description: 'Pendant panic button activated by patient.'
    };
    setSafetyEvents(prev => [newSafetyEvent, ...prev]);
    addTimelineEvent('🚨 SOS Button Activated', 'Patient pressed emergency button on pendant.', 'safety', 'alert', 'AlertTriangle');
    setNotifications(prev => [
      {
        id: 'notif-sos-' + Date.now(),
        title: '🚨 CRITICAL SOS ALERT',
        message: 'Raghavan pressed the Pendant SOS button at home.',
        timestamp: 'Just now',
        read: false,
        type: 'safety'
      },
      ...prev
    ]);
  };

  const simulateGeofenceExit = () => {
    addToast('📍 DEMO SIMULATION: Safe Zone Boundary Exit Detected', 'alert');
    setPatient(prev => ({ ...prev, status: 'attention' }));
    setLocation(prev => ({
      ...prev,
      status: 'safe_zone_exit',
      address: 'Near East Gate Alleyway (180m from home)',
      coordinates: { lat: 12.9268, lng: 77.6872 },
      lastUpdated: 'Just now'
    }));
    const newSafetyEvent: SafetyEvent = {
      id: 'safe-geo-' + Date.now(),
      timestamp: 'Just now',
      type: 'geofence_exit',
      severity: 'high',
      resolved: false,
      description: 'Patient left 150m safe perimeter around 42 Jasmine Gardens.'
    };
    setSafetyEvents(prev => [newSafetyEvent, ...prev]);
    addTimelineEvent('📍 Safe Zone Exit Alert', 'Patient crossed 150m safe perimeter.', 'location', 'alert', 'MapPin');
  };

  const simulateReturnHome = () => {
    addToast('🏡 Patient Returned to Safe Home Zone', 'success');
    setPatient(prev => ({ ...prev, status: 'stable' }));
    setLocation(prev => ({
      ...prev,
      status: 'at_home',
      address: '42 Jasmine Gardens, Green Glen Layout, Bengaluru',
      coordinates: { lat: 12.925, lng: 77.685 },
      lastUpdated: 'Just now'
    }));
    addTimelineEvent('Location Normal', 'Patient returned safely to home safe-zone.', 'location', 'success', 'Home');
  };

  const simulatePersonDetected = (personName: string, relation: string) => {
    addToast(`📹 Camera Detected: ${personName} (${relation})`, 'info');
    const newRec: RecognitionEvent = {
      id: 'rec-' + Date.now(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      personName,
      relation,
      confidenceScore: 99.1,
      cameraLocation: 'Front Entrance Cam',
      status: 'recognized'
    };
    setRecognitionEvents(prev => [newRec, ...prev]);
    addTimelineEvent('Familiar Person Detected', `${personName} (${relation}) recognized at entrance.`, 'camera', 'info', 'UserCheck');
  };

  const simulateUnknownPersonDetected = () => {
    addToast('⚠️ Camera Alert: Unrecognized Visitor at Doorstep', 'warning');
    const newRec: RecognitionEvent = {
      id: 'rec-unk-' + Date.now(),
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      personName: 'Unidentified Person',
      relation: 'Unknown Visitor',
      confidenceScore: 42.0,
      cameraLocation: 'Front Door Camera',
      status: 'unknown_visitor'
    };
    setRecognitionEvents(prev => [newRec, ...prev]);
    addTimelineEvent('Unidentified Visitor', 'Camera detected unrecognized person at doorstep.', 'camera', 'warning', 'UserX');
  };

  const simulateGenerateNewRecommendation = () => {
    const newRec: AIRecommendation = {
      id: 'ai-gen-' + Date.now(),
      title: 'Warm Herbal Tea & Reminiscence Storytelling',
      activityType: 'Calm Sensory Care',
      durationMinutes: 15,
      reason: 'Observed activity pattern suggests evening calm tea routine reduces night restlessness.',
      recommendedTime: 'In 10 mins',
      status: 'suggested',
      icon: 'Coffee'
    };
    setAiRecommendations(prev => [newRec, ...prev]);
    addToast('🌱 AI Companion generated a new activity recommendation!', 'success');
    addTimelineEvent('AI Care Suggestion Created', newRec.title, 'activities', 'info', 'Sparkles');
  };

  const resetSimulations = () => {
    setPatient(initialPatient);
    setMedications(initialMedications);
    setRoutines(initialRoutines);
    setHabilitation(initialHabilitationActivities);
    setCognitive(initialCognitiveActivities);
    setObservations(initialObservations);
    setLocation(initialLocation);
    setSafetyEvents(initialSafetyEvents);
    setPendant(initialPendant);
    setRecognitionEvents(initialRecognitionEvents);
    setAiRecommendations(initialAIRecommendations);
    setTimelineEvents(initialTimelineEvents);
    setNotifications(initialNotifications);
    addToast('Reset mock data to initial stable state.', 'info');
  };

  return (
    <AppStateContext.Provider
      value={{
        activeTab,
        setActiveTab,
        isPhoneFrame,
        setIsPhoneFrame,
        patient,
        medications,
        routines,
        habilitation,
        cognitive,
        observations,
        appointments,
        location,
        movement,
        sleep,
        safetyEvents,
        pendant,
        familiarPeople,
        recognitionEvents,
        aiRecommendations,
        aiInsights,
        timelineEvents,
        reports,
        notifications,
        toasts,
        addToast,
        removeToast,
        markMedicationTaken,
        markMedicationMissed,
        toggleHabilitation,
        toggleCognitive,
        logBehaviourObservation,
        completeAiRecommendation,
        simulateMedicationReminder,
        simulateSOS,
        simulateGeofenceExit,
        simulateReturnHome,
        simulatePersonDetected,
        simulateUnknownPersonDetected,
        simulateGenerateNewRecommendation,
        resetSimulations
      }}
    >
      {children}
    </AppStateContext.Provider>
  );
};

export const useAppState = () => {
  const context = useContext(AppStateContext);
  if (!context) {
    throw new Error('useAppState must be used within an AppStateProvider');
  }
  return context;
};
