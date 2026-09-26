export type PatientStatus = 'stable' | 'attention' | 'critical';

export interface Patient {
  id: string;
  name: string;
  age: number;
  condition: string;
  stage: string;
  status: PatientStatus;
  primaryCaregiver: string;
  primaryCaregiverRelation: string;
  secondaryCaregiver: string;
  secondaryCaregiverRelation: string;
  doctorName: string;
  doctorSpecialty: string;
  avatarUrl: string;
  emergencyContact: string;
}

export type MedicationStatus = 'taken' | 'pending' | 'missed' | 'snoozed';

export interface Medication {
  id: string;
  name: string;
  dosage: string;
  scheduledTime: string;
  status: MedicationStatus;
  instructions: string;
  icon?: string;
}

export interface MedicationEvent {
  id: string;
  medicationId: string;
  medicationName: string;
  dosage: string;
  timestamp: string;
  status: MedicationStatus;
  acknowledgedBy?: string;
}

export interface RoutineItem {
  id: string;
  title: string;
  category: 'medication' | 'activities' | 'cognitive' | 'hydration' | 'nutrition' | 'behaviour';
  completed: number;
  total: number;
}

export interface HabilitationActivity {
  id: string;
  title: string;
  category: string;
  durationMinutes: number;
  completed: boolean;
  scheduledTime: string;
}

export interface CognitiveActivity {
  id: string;
  title: string;
  type: string;
  durationMinutes: number;
  completed: boolean;
  score?: string;
}

export interface BehaviourObservation {
  id: string;
  timestamp: string;
  type: 'calm' | 'confusion' | 'agitation' | 'repetitive_questioning' | 'wandering';
  note: string;
  intensity: 'mild' | 'moderate' | 'severe';
  caregiverActionTaken?: string;
}

export interface Appointment {
  id: string;
  title: string;
  doctor: string;
  specialty: string;
  date: string;
  time: string;
  location: string;
  status: 'upcoming' | 'completed' | 'cancelled';
}

export interface LocationData {
  status: 'at_home' | 'safe_zone_exit' | 'wandering';
  address: string;
  coordinates: { lat: number; lng: number };
  safeZoneCenter: { lat: number; lng: number };
  safeZoneRadiusMeters: number;
  lastUpdated: string;
  batteryLevel: number;
}

export interface MovementData {
  dailyKm: number;
  steps: number;
  activityLevel: 'low' | 'normal' | 'active';
  lastMovementTime: string;
}

export interface SleepData {
  durationHours: number;
  quality: 'restful' | 'restless' | 'interrupted';
  sleepStart: string;
  sleepEnd: string;
  nightWakeups: number;
}

export interface SafetyEvent {
  id: string;
  timestamp: string;
  type: 'sos_button' | 'fall_detected' | 'geofence_exit' | 'pendant_disconnected';
  severity: 'low' | 'medium' | 'high' | 'critical';
  resolved: boolean;
  description: string;
}

export interface FamiliarPerson {
  id: string;
  name: string;
  relation: string;
  avatar: string;
  lastRecognized?: string;
  status: 'frequent' | 'recent' | 'visitor';
}

export interface RecognitionEvent {
  id: string;
  timestamp: string;
  personName: string;
  relation: string;
  confidenceScore: number;
  cameraLocation: string;
  status: 'recognized' | 'unknown_visitor';
}

export interface PendantStatus {
  connected: boolean;
  batteryLevel: number;
  gpsStatus: 'available' | 'low_accuracy' | 'unavailable';
  speakerStatus: 'working' | 'muted';
  lastSync: string;
  remindersActive: boolean;
}

export interface AIRecommendation {
  id: string;
  title: string;
  activityType: string;
  durationMinutes: number;
  reason: string;
  recommendedTime: string;
  status: 'suggested' | 'started' | 'completed' | 'not_suitable';
  icon: string;
  observed?: string;
  whyItMatters?: string;
  suggestedAction?: string;
  whyThisActivity?: string;
  safetyCarePlan?: string;
  expectedOutcome?: string;
  caregiverFeedback?: string;
}

export interface AIInsight {
  id: string;
  category: 'sleep' | 'activity' | 'medication' | 'mood';
  title: string;
  description: string;
  timestamp: string;
  metric?: string;
}

export type EventCategory = 'all' | 'medication' | 'activities' | 'behaviour' | 'safety' | 'location' | 'camera' | 'care_plan';

export interface TimelineEvent {
  id: string;
  timestamp: string;
  timeDisplay: string;
  title: string;
  description: string;
  category: EventCategory;
  severity?: 'info' | 'warning' | 'alert' | 'success';
  iconName: string;
}

export interface CareReport {
  id: string;
  title: string;
  type: 'weekly' | 'monthly' | 'doctor' | 'medication' | 'activity' | 'safety';
  generatedDate: string;
  period: string;
  summary: string;
  adherenceRate: number;
  medicationRate: number;
  cognitiveRate: number;
  fileSize: string;
}

export interface NotificationItem {
  id: string;
  title: string;
  message: string;
  timestamp: string;
  read: boolean;
  type: 'medication' | 'safety' | 'ai' | 'system';
}

export type NavigationTab = 'home' | 'care' | 'medication' | 'monitor' | 'insights' | 'ai-companion' | 'timeline' | 'reports' | 'more';
