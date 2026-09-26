import { apiClient, setAuthToken } from './apiClient';
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
  NotificationItem,
  EventCategory
} from '../types';

export const PATIENT_ID = 'pat-101';

// Demo configuration isolation (Section 5 & 23)
const IS_DEMO_MODE = import.meta.env.VITE_DEMO_MODE !== 'false';
const DEMO_EMAIL = import.meta.env.VITE_DEMO_CAREGIVER_EMAIL || 'anu.menon@carecompanion.in';
const DEMO_PASSWORD = import.meta.env.VITE_DEMO_CAREGIVER_PASSWORD || 'password123';

export const authService = {
  login: async (email?: string, password?: string) => {
    const loginEmail = email || (IS_DEMO_MODE ? DEMO_EMAIL : '');
    const loginPassword = password || (IS_DEMO_MODE ? DEMO_PASSWORD : '');

    if (!loginEmail || !loginPassword) {
      return null;
    }

    try {
      const res = await apiClient.post<{ access_token: string; role: string; name: string; patient_id: string }>(
        '/auth/login',
        { email: loginEmail, password: loginPassword }
      );
      if (res.access_token) {
        setAuthToken(res.access_token);
      }
      return res;
    } catch {
      return null;
    }
  },
  getMe: async () => {
    try {
      return await apiClient.get<any>('/auth/me');
    } catch {
      return null;
    }
  }
};

export const patientService = {
  getPatient: async (patientId: string = PATIENT_ID): Promise<Patient> => {
    try {
      return await apiClient.get<Patient>(`/patients/${patientId}`);
    } catch {
      return initialPatient;
    }
  },
  updateStatus: async (status: Patient['status'], patientId: string = PATIENT_ID): Promise<Patient> => {
    try {
      return await apiClient.put<Patient>(`/patients/${patientId}/status`, { status });
    } catch {
      return { ...initialPatient, status };
    }
  },
  getDashboard: async (patientId: string = PATIENT_ID) => {
    try {
      return await apiClient.get<any>(`/patients/${patientId}/dashboard`);
    } catch {
      return null;
    }
  }
};

export const medicationService = {
  getMedications: async (patientId: string = PATIENT_ID): Promise<Medication[]> => {
    try {
      return await apiClient.get<Medication[]>(`/patients/${patientId}/medications`);
    } catch {
      return initialMedications;
    }
  },
  markTaken: async (meds: Medication[], id: string, patientId: string = PATIENT_ID): Promise<Medication[]> => {
    try {
      const updated = await apiClient.post<Medication>(`/patients/${patientId}/medications/${id}/acknowledge`, { status: 'taken' });
      return meds.map(m => (m.id === id ? updated : m));
    } catch {
      return meds.map(m => (m.id === id ? { ...m, status: 'taken' as const } : m));
    }
  },
  markMissed: async (meds: Medication[], id: string, patientId: string = PATIENT_ID): Promise<Medication[]> => {
    try {
      const updated = await apiClient.post<Medication>(`/patients/${patientId}/medications/${id}/miss`);
      return meds.map(m => (m.id === id ? updated : m));
    } catch {
      return meds.map(m => (m.id === id ? { ...m, status: 'missed' as const } : m));
    }
  },
  createMedication: async (patientId: string, medData: Partial<Medication>): Promise<Medication> => {
    return await apiClient.post<Medication>(`/patients/${patientId}/medications`, medData);
  }
};

export const careService = {
  getRoutines: async (patientId: string = PATIENT_ID): Promise<RoutineItem[]> => {
    try {
      return await apiClient.get<RoutineItem[]>(`/patients/${patientId}/care/routines`);
    } catch {
      return initialRoutines;
    }
  },
  getHabilitation: async (patientId: string = PATIENT_ID): Promise<HabilitationActivity[]> => {
    try {
      return await apiClient.get<HabilitationActivity[]>(`/patients/${patientId}/care/habilitation`);
    } catch {
      return initialHabilitationActivities;
    }
  },
  toggleHabilitation: async (activityId: string, patientId: string = PATIENT_ID): Promise<HabilitationActivity> => {
    return await apiClient.post<HabilitationActivity>(`/patients/${patientId}/care/habilitation/${activityId}/toggle`);
  },
  getCognitive: async (patientId: string = PATIENT_ID): Promise<CognitiveActivity[]> => {
    try {
      return await apiClient.get<CognitiveActivity[]>(`/patients/${patientId}/care/cognitive`);
    } catch {
      return initialCognitiveActivities;
    }
  },
  toggleCognitive: async (activityId: string, patientId: string = PATIENT_ID): Promise<CognitiveActivity> => {
    return await apiClient.post<CognitiveActivity>(`/patients/${patientId}/care/cognitive/${activityId}/toggle`);
  },
  getObservations: async (patientId: string = PATIENT_ID): Promise<BehaviourObservation[]> => {
    try {
      return await apiClient.get<BehaviourObservation[]>(`/patients/${patientId}/care/observations`);
    } catch {
      return initialObservations;
    }
  },
  logObservation: async (
    type: BehaviourObservation['type'],
    note: string,
    intensity: BehaviourObservation['intensity'] = 'mild',
    patientId: string = PATIENT_ID
  ): Promise<BehaviourObservation> => {
    return await apiClient.post<BehaviourObservation>(`/patients/${patientId}/care/observations`, {
      type,
      note,
      intensity,
      caregiverActionTaken: 'Logged & observed by caregiver.'
    });
  },
  getAppointments: async (patientId: string = PATIENT_ID): Promise<Appointment[]> => {
    try {
      return await apiClient.get<Appointment[]>(`/patients/${patientId}/care/appointments`);
    } catch {
      return initialAppointments;
    }
  },
  logHydration: async (amount: number = 1, patientId: string = PATIENT_ID) => {
    return await apiClient.post<{ id: string; amount: number; unit: string; recordedAt: string; todayTotal: number }>(
      `/patients/${patientId}/care/hydration`,
      { amount, unit: 'glass' }
    );
  },
  logMeal: async (mealType: string = 'snack', intakeLevel: string = 'good', notes: string = '', patientId: string = PATIENT_ID) => {
    return await apiClient.post<{ id: string; mealType: string; intakeLevel: string; recordedAt: string; notes?: string }>(
      `/patients/${patientId}/care/nutrition`,
      { mealType, intakeLevel, notes }
    );
  }
};

export const monitoringService = {
  getSummary: async (patientId: string = PATIENT_ID) => {
    try {
      return await apiClient.get<any>(`/patients/${patientId}/monitoring/summary`);
    } catch {
      return null;
    }
  },
  getLocation: async (patientId: string = PATIENT_ID): Promise<LocationData> => {
    try {
      return await apiClient.get<LocationData>(`/patients/${patientId}/monitoring/location`);
    } catch {
      return initialLocation;
    }
  },
  getMovement: async (patientId: string = PATIENT_ID): Promise<MovementData> => {
    try {
      return await apiClient.get<MovementData>(`/patients/${patientId}/monitoring/movement`);
    } catch {
      return initialMovement;
    }
  },
  getSleep: async (patientId: string = PATIENT_ID): Promise<SleepData> => {
    try {
      return await apiClient.get<SleepData>(`/patients/${patientId}/monitoring/sleep`);
    } catch {
      return initialSleep;
    }
  },
  getSafetyEvents: async (patientId: string = PATIENT_ID): Promise<SafetyEvent[]> => {
    try {
      return await apiClient.get<SafetyEvent[]>(`/patients/${patientId}/monitoring/safety`);
    } catch {
      return initialSafetyEvents;
    }
  },
  triggerSOS: async (patientId: string = PATIENT_ID): Promise<SafetyEvent> => {
    return await apiClient.post<SafetyEvent>(`/patients/${patientId}/monitoring/safety/sos`);
  },
  getFamiliarPeople: async (patientId: string = PATIENT_ID): Promise<FamiliarPerson[]> => {
    try {
      return await apiClient.get<FamiliarPerson[]>(`/patients/${patientId}/camera/familiar-people`);
    } catch {
      return initialFamiliarPeople;
    }
  },
  getRecognitionEvents: async (patientId: string = PATIENT_ID): Promise<RecognitionEvent[]> => {
    try {
      return await apiClient.get<RecognitionEvent[]>(`/patients/${patientId}/camera/recognitions`);
    } catch {
      return initialRecognitionEvents;
    }
  }
};

export const pendantService = {
  getPendantStatus: async (patientId: string = PATIENT_ID): Promise<PendantStatus> => {
    try {
      return await apiClient.get<PendantStatus>(`/patients/${patientId}/monitoring/pendant`);
    } catch {
      return initialPendant;
    }
  },
  testReminder: async (patientId: string = PATIENT_ID) => {
    return await apiClient.post<{ success: boolean; message: string }>(
      `/patients/${patientId}/monitoring/pendant/test-reminder`
    );
  }
};

export const aiService = {
  getRecommendations: async (patientId: string = PATIENT_ID): Promise<AIRecommendation[]> => {
    try {
      return await apiClient.get<AIRecommendation[]>(`/patients/${patientId}/ai/recommendations`);
    } catch {
      return initialAIRecommendations;
    }
  },
  getInsights: async (patientId: string = PATIENT_ID): Promise<AIInsight[]> => {
    try {
      return await apiClient.get<AIInsight[]>(`/patients/${patientId}/ai/insights`);
    } catch {
      return initialAIInsights;
    }
  },
  completeRecommendation: async (recId: string, feedback: string = 'enjoyed', patientId: string = PATIENT_ID): Promise<AIRecommendation> => {
    return await apiClient.post<AIRecommendation>(
      `/patients/${patientId}/ai/recommendations/${recId}/complete`,
      { feedback }
    );
  },
  recordFeedback: async (recId: string, feedback: string, patientId: string = PATIENT_ID) => {
    return await apiClient.post<AIRecommendation>(`/patients/${patientId}/ai/recommendations/${recId}/feedback`, {
      feedback
    });
  },
  generateRecommendation: async (patientId: string = PATIENT_ID): Promise<AIRecommendation> => {
    return await apiClient.post<AIRecommendation>(`/patients/${patientId}/ai/generate-summary`);
  }
};

export const reportService = {
  getReports: async (patientId: string = PATIENT_ID): Promise<CareReport[]> => {
    try {
      return await apiClient.get<CareReport[]>(`/patients/${patientId}/reports`);
    } catch {
      return initialReports;
    }
  },
  generateReport: async (reportType: string = 'doctor', period: string = 'Last 30 Days', patientId: string = PATIENT_ID): Promise<CareReport> => {
    return await apiClient.post<CareReport>(`/patients/${patientId}/reports/generate`, {
      report_type: reportType,
      period
    });
  },
  downloadReportPDF: async (reportId: string, title: string = 'CareReport', patientId: string = PATIENT_ID): Promise<void> => {
    const filename = `${title.replace(/\s+/g, '_')}_${reportId}.pdf`;
    await apiClient.downloadBlob(`/patients/${patientId}/reports/${reportId}/download`, filename);
  },
  getNotifications: async (patientId: string = PATIENT_ID): Promise<NotificationItem[]> => {
    try {
      return await apiClient.get<NotificationItem[]>(`/patients/${patientId}/notifications`);
    } catch {
      return initialNotifications;
    }
  },
  markNotificationRead: async (notifId: string, patientId: string = PATIENT_ID) => {
    return await apiClient.put<NotificationItem>(`/patients/${patientId}/notifications/${notifId}/read`);
  },
  getTimelineEvents: async (category: EventCategory = 'all', patientId: string = PATIENT_ID): Promise<TimelineEvent[]> => {
    try {
      return await apiClient.get<TimelineEvent[]>(`/patients/${patientId}/timeline?category=${category}&limit=50`);
    } catch {
      return initialTimelineEvents;
    }
  }
};

export const cameraService = {
  recordRecognition: async (payload: {
    patient_id?: string;
    detected_name: string;
    relation: string;
    confidence: number;
    camera_location?: string;
  }): Promise<RecognitionEvent> => {
    return await apiClient.post<RecognitionEvent>('/camera/recognitions', {
      patient_id: payload.patient_id || PATIENT_ID,
      ...payload
    });
  }
};

export const simulationService = {
  simulateMedicationReminder: async (patientId: string = PATIENT_ID) => {
    return await apiClient.post<{ success: boolean; message: string }>(`/simulation/pendant/reminder?patient_id=${patientId}`);
  },
  simulateSOS: async (patientId: string = PATIENT_ID) => {
    return await apiClient.post<{ success: boolean; message: string }>(`/simulation/pendant/sos?patient_id=${patientId}`);
  },
  simulateLowBattery: async (patientId: string = PATIENT_ID) => {
    return await apiClient.post<{ success: boolean; message: string }>(`/simulation/pendant/low-battery?patient_id=${patientId}`);
  },
  simulateGeofenceExit: async (patientId: string = PATIENT_ID) => {
    return await apiClient.post<{ success: boolean; message: string }>(`/simulation/pendant/geofence?patient_id=${patientId}`);
  },
  simulateReturnHome: async (patientId: string = PATIENT_ID) => {
    return await apiClient.post<{ success: boolean; message: string }>(`/simulation/pendant/return-home?patient_id=${patientId}`);
  },
  resolveSafetyAlert: async (patientId: string = PATIENT_ID) => {
    return await apiClient.post<{ success: boolean; message: string }>(`/simulation/safety/resolve?patient_id=${patientId}`);
  },
  simulatePersonDetected: async (personName: string, relation: string, patientId: string = PATIENT_ID) => {
    return await apiClient.post<{ success: boolean; message: string }>(
      `/simulation/camera/recognition?patient_id=${patientId}`,
      { personName, relation, confidence: 99.1, cameraLocation: 'Front Entrance Cam' }
    );
  },
  simulateUnknownPersonDetected: async (patientId: string = PATIENT_ID) => {
    return await apiClient.post<{ success: boolean; message: string }>(`/simulation/camera/unknown?patient_id=${patientId}`);
  },
  simulateNewRecommendation: async (patientId: string = PATIENT_ID) => {
    return await apiClient.post<{ success: boolean; message: string }>(`/simulation/ai/recommendation?patient_id=${patientId}`);
  },
  resetSimulations: async (patientId: string = PATIENT_ID) => {
    return await apiClient.post<{ success: boolean; message: string }>(`/simulation/reset?patient_id=${patientId}`);
  }
};

