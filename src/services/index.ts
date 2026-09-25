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
  NotificationItem
} from '../types';

export const patientService = {
  getPatient: async (): Promise<Patient> => initialPatient,
  updateStatus: async (status: Patient['status']): Promise<Patient> => ({ ...initialPatient, status })
};

export const medicationService = {
  getMedications: async (): Promise<Medication[]> => initialMedications,
  markTaken: (meds: Medication[], id: string): Medication[] =>
    meds.map(m => (m.id === id ? { ...m, status: 'taken' as const } : m)),
  markMissed: (meds: Medication[], id: string): Medication[] =>
    meds.map(m => (m.id === id ? { ...m, status: 'missed' as const } : m))
};

export const careService = {
  getRoutines: async (): Promise<RoutineItem[]> => initialRoutines,
  getHabilitation: async (): Promise<HabilitationActivity[]> => initialHabilitationActivities,
  getCognitive: async (): Promise<CognitiveActivity[]> => initialCognitiveActivities,
  getObservations: async (): Promise<BehaviourObservation[]> => initialObservations,
  getAppointments: async (): Promise<Appointment[]> => initialAppointments
};

export const monitoringService = {
  getLocation: async (): Promise<LocationData> => initialLocation,
  getMovement: async (): Promise<MovementData> => initialMovement,
  getSleep: async (): Promise<SleepData> => initialSleep,
  getSafetyEvents: async (): Promise<SafetyEvent[]> => initialSafetyEvents,
  getFamiliarPeople: async (): Promise<FamiliarPerson[]> => initialFamiliarPeople,
  getRecognitionEvents: async (): Promise<RecognitionEvent[]> => initialRecognitionEvents
};

export const pendantService = {
  getPendantStatus: async (): Promise<PendantStatus> => initialPendant
};

export const aiService = {
  getRecommendations: async (): Promise<AIRecommendation[]> => initialAIRecommendations,
  getInsights: async (): Promise<AIInsight[]> => initialAIInsights
};

export const reportService = {
  getReports: async (): Promise<CareReport[]> => initialReports,
  getNotifications: async (): Promise<NotificationItem[]> => initialNotifications,
  getTimelineEvents: async (): Promise<TimelineEvent[]> => initialTimelineEvents
};
