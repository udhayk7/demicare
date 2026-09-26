import React, { createContext, useContext, useState, useEffect } from 'react';
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
import {
  authService,
  patientService,
  medicationService,
  careService,
  monitoringService,
  aiService,
  reportService,
  simulationService,
  PATIENT_ID
} from '../services';

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
  logHydration: (amount?: number) => void;
  logMeal: (mealType?: string, intake?: string) => void;
  completeAiRecommendation: (id: string, feedback?: string) => void;
  
  // Simulations
  simulateMedicationReminder: () => void;
  simulateSOS: () => void;
  simulateLowBattery: () => void;
  simulateGeofenceExit: () => void;
  simulateReturnHome: () => void;
  resolveSafetyAlert: () => void;
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
  const [appointments, setAppointments] = useState<Appointment[]>(initialAppointments);
  
  const [location, setLocation] = useState<LocationData>(initialLocation);
  const [movement, setMovement] = useState<MovementData>(initialMovement);
  const [sleep, setSleep] = useState<SleepData>(initialSleep);
  const [safetyEvents, setSafetyEvents] = useState<SafetyEvent[]>(initialSafetyEvents);
  const [pendant, setPendant] = useState<PendantStatus>(initialPendant);
  const [familiarPeople, setFamiliarPeople] = useState<FamiliarPerson[]>(initialFamiliarPeople);
  const [recognitionEvents, setRecognitionEvents] = useState<RecognitionEvent[]>(initialRecognitionEvents);
  
  const [aiRecommendations, setAiRecommendations] = useState<AIRecommendation[]>(initialAIRecommendations);
  const [aiInsights, setAiInsights] = useState<AIInsight[]>(initialAIInsights);
  const [timelineEvents, setTimelineEvents] = useState<TimelineEvent[]>(initialTimelineEvents);
  const [reports, setReports] = useState<CareReport[]>(initialReports);
  const [notifications, setNotifications] = useState<NotificationItem[]>(initialNotifications);
  const [toasts, setToasts] = useState<Toast[]>([]);

  // Initial Sync from Backend
  useEffect(() => {
    const initBackend = async () => {
      try {
        await authService.login();
        
        // Load initial dashboard
        const dash = await patientService.getDashboard(PATIENT_ID);
        if (dash) {
          if (dash.patient) setPatient(dash.patient);
          if (dash.medications) setMedications(dash.medications);
          if (dash.routines) setRoutines(dash.routines);
          if (dash.location) setLocation(dash.location);
          if (dash.movement) setMovement(dash.movement);
          if (dash.sleep) setSleep(dash.sleep);
          if (dash.pendant) setPendant(dash.pendant);
        }

        // Load timeline, habilitation, cognitive, reports, observations, safety & camera in background
        const [tl, hab, cog, reps, notifs, people, recs, insights, apps, obs, safes, rec_evts] = await Promise.all([
          reportService.getTimelineEvents('all', PATIENT_ID),
          careService.getHabilitation(PATIENT_ID),
          careService.getCognitive(PATIENT_ID),
          reportService.getReports(PATIENT_ID),
          reportService.getNotifications(PATIENT_ID),
          monitoringService.getFamiliarPeople(PATIENT_ID),
          aiService.getRecommendations(PATIENT_ID),
          aiService.getInsights(PATIENT_ID),
          careService.getAppointments(PATIENT_ID),
          careService.getObservations(PATIENT_ID),
          monitoringService.getSafetyEvents(PATIENT_ID),
          monitoringService.getRecognitionEvents(PATIENT_ID)
        ]);

        if (tl && tl.length) setTimelineEvents(tl);
        if (hab && hab.length) setHabilitation(hab);
        if (cog && cog.length) setCognitive(cog);
        if (reps && reps.length) setReports(reps);
        if (notifs && notifs.length) setNotifications(notifs);
        if (people && people.length) setFamiliarPeople(people);
        if (recs && recs.length) setAiRecommendations(recs);
        if (insights && insights.length) setAiInsights(insights);
        if (apps && apps.length) setAppointments(apps);
        if (obs && obs.length) setObservations(obs);
        if (safes && safes.length) setSafetyEvents(safes);
        if (rec_evts && rec_evts.length) setRecognitionEvents(rec_evts);
      } catch (err) {
        console.warn('Backend sync initialized with fallback data:', err);
      }
    };

    initBackend();
  }, []);

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

    // Async persist to Backend
    medicationService.markTaken(medications, id, PATIENT_ID).catch(err => {
      console.error('Failed to sync medication acknowledge:', err);
    });
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

    // Async persist to Backend
    medicationService.markMissed(medications, id, PATIENT_ID).catch(err => {
      console.error('Failed to sync medication missed:', err);
    });
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

    // Async persist to Backend
    careService.toggleHabilitation(id, PATIENT_ID).catch(err => {
      console.error('Failed to sync habilitation toggle:', err);
    });
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

    // Async persist to Backend
    careService.toggleCognitive(id, PATIENT_ID).catch(err => {
      console.error('Failed to sync cognitive toggle:', err);
    });
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

    // Async persist to Backend
    careService.logObservation(type, note, intensity, PATIENT_ID).catch(err => {
      console.error('Failed to sync observation:', err);
    });
  };

  const logHydration = (amount: number = 1) => {
    setRoutines(prev =>
      prev.map(r => (r.category === 'hydration' ? { ...r, completed: Math.min(r.total, r.completed + amount) } : r))
    );
    addToast(`Logged ${amount} glass of water.`, 'success');
    addTimelineEvent('Hydration Logged', `Logged ${amount} glass of water for Raghavan.`, 'activities', 'success', 'Droplets');
    careService.logHydration(amount, PATIENT_ID).catch(err => {
      console.error('Failed to sync hydration:', err);
    });
  };

  const logMeal = (mealType: string = 'snack', intake: string = 'good') => {
    setRoutines(prev =>
      prev.map(r => (r.category === 'nutrition' ? { ...r, completed: Math.min(r.total, r.completed + 1) } : r))
    );
    addToast(`Logged ${mealType} (${intake} intake).`, 'success');
    addTimelineEvent('Meal Logged', `Logged ${mealType} with ${intake} intake.`, 'activities', 'success', 'Utensils');
    careService.logMeal(mealType, intake, '', PATIENT_ID).catch(err => {
      console.error('Failed to sync meal:', err);
    });
  };

  const completeAiRecommendation = (id: string, feedback: string = 'enjoyed') => {
    let title = '';
    setAiRecommendations(prev =>
      prev.map(r => {
        if (r.id === id) {
          title = r.title;
          return { ...r, status: 'completed' as const, caregiverFeedback: feedback };
        }
        return r;
      })
    );
    const feedbackLabel = feedback === 'enjoyed' ? 'Patient Enjoyed It' : feedback === 'disliked' ? 'Patient Disliked' : feedback === 'tired' ? 'Patient Became Tired' : feedback;
    addToast(`AI Activity "${title}" recorded (${feedbackLabel})!`, 'success');
    addTimelineEvent('AI Activity Completed', `${title} — Outcome recorded: ${feedbackLabel}`, 'activities', 'success', 'Sparkles');

    // Async persist to Backend
    aiService.completeRecommendation(id, feedback, PATIENT_ID).catch(err => {
      console.error('Failed to sync AI recommendation complete:', err);
    });
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

    // Backend trigger
    simulationService.simulateMedicationReminder(PATIENT_ID).catch(err => {
      console.error('Simulate med reminder error:', err);
    });
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

    // Backend trigger
    simulationService.simulateSOS(PATIENT_ID).catch(err => {
      console.error('Simulate SOS error:', err);
    });
  };

  const simulateLowBattery = () => {
    addToast('⚠️ DEMO SIMULATION: Low Pendant Battery (14%)', 'warning');
    setPendant(prev => ({ ...prev, batteryLevel: 14 }));
    addTimelineEvent('⚠️ Low Battery Alert', 'Pendant battery dropped to 14%. Needs charging dock.', 'safety', 'warning', 'BatteryLow');
    setNotifications(prev => [
      {
        id: 'notif-bat-' + Date.now(),
        title: '⚠️ Low Pendant Battery (14%)',
        message: "Raghavan's pendant dropped below 15%. Please place on charging dock.",
        timestamp: 'Just now',
        read: false,
        type: 'safety'
      },
      ...prev
    ]);

    simulationService.simulateLowBattery(PATIENT_ID).catch(err => {
      console.error('Simulate low battery error:', err);
    });
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

    // Backend trigger
    simulationService.simulateGeofenceExit(PATIENT_ID).catch(err => {
      console.error('Simulate geofence exit error:', err);
    });
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

    // Backend trigger
    simulationService.simulateReturnHome(PATIENT_ID).catch(err => {
      console.error('Simulate return home error:', err);
    });
  };

  const resolveSafetyAlert = () => {
    addToast('✓ Active emergency alerts resolved', 'success');
    setPatient(prev => ({ ...prev, status: 'stable' }));
    setSafetyEvents(prev => prev.map(s => ({ ...s, resolved: true })));
    addTimelineEvent('Alert Resolved', 'Caregiver resolved active safety alarm.', 'safety', 'success', 'ShieldCheck');

    simulationService.resolveSafetyAlert(PATIENT_ID).catch(err => {
      console.error('Resolve safety alert error:', err);
    });
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

    // Backend trigger
    simulationService.simulatePersonDetected(personName, relation, PATIENT_ID).catch(err => {
      console.error('Simulate person detected error:', err);
    });
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

    // Backend trigger
    simulationService.simulateUnknownPersonDetected(PATIENT_ID).catch(err => {
      console.error('Simulate unknown person error:', err);
    });
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

    // Backend trigger
    simulationService.simulateNewRecommendation(PATIENT_ID).catch(err => {
      console.error('Simulate AI recommendation error:', err);
    });
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

    // Backend trigger
    simulationService.resetSimulations(PATIENT_ID).catch(err => {
      console.error('Reset simulations error:', err);
    });
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
        logHydration,
        logMeal,
        completeAiRecommendation,
        simulateMedicationReminder,
        simulateSOS,
        simulateLowBattery,
        simulateGeofenceExit,
        simulateReturnHome,
        resolveSafetyAlert,
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
