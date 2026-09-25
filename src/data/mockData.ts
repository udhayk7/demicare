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

export const initialPatient: Patient = {
  id: 'pat-101',
  name: 'Raghavan Menon',
  age: 72,
  condition: 'Mild-to-Moderate Dementia',
  stage: 'Stage 2 · Moderate',
  status: 'stable',
  primaryCaregiver: 'Anu Menon',
  primaryCaregiverRelation: 'Daughter',
  secondaryCaregiver: 'Suresh Menon',
  secondaryCaregiverRelation: 'Son',
  doctorName: 'Dr. Arun Nair',
  doctorSpecialty: 'Neurologist (Cognitive Care)',
  avatarUrl: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&q=80&w=200',
  emergencyContact: '+91 98450 12345'
};

export const initialMedications: Medication[] = [
  {
    id: 'med-1',
    name: 'Donepezil',
    dosage: '5 mg',
    scheduledTime: '08:00',
    status: 'taken',
    instructions: 'Take 1 tablet after morning breakfast with warm water',
    icon: 'Pill'
  },
  {
    id: 'med-2',
    name: 'Vitamin D3 & Calcium',
    dosage: '1000 IU',
    scheduledTime: '13:00',
    status: 'taken',
    instructions: 'Take 1 capsule after lunch',
    icon: 'Sun'
  },
  {
    id: 'med-3',
    name: 'Memantine',
    dosage: '10 mg',
    scheduledTime: '18:00',
    status: 'missed',
    instructions: 'Take 1 tablet before evening tea',
    icon: 'HeartPulse'
  },
  {
    id: 'med-4',
    name: 'Donepezil',
    dosage: '5 mg',
    scheduledTime: '21:00',
    status: 'pending',
    instructions: 'Take 1 tablet 30 minutes before sleep',
    icon: 'Moon'
  },
  {
    id: 'med-5',
    name: 'Melatonin',
    dosage: '3 mg',
    scheduledTime: '21:30',
    status: 'pending',
    instructions: 'Take as needed for sleep routine support',
    icon: 'Sparkles'
  }
];

export const initialRoutines: RoutineItem[] = [
  { id: 'rout-1', title: 'Medication', category: 'medication', completed: 4, total: 5 },
  { id: 'rout-2', title: 'Activities', category: 'activities', completed: 6, total: 7 },
  { id: 'rout-3', title: 'Cognitive', category: 'cognitive', completed: 2, total: 3 },
  { id: 'rout-4', title: 'Hydration', category: 'hydration', completed: 5, total: 7 },
  { id: 'rout-5', title: 'Nutrition', category: 'nutrition', completed: 3, total: 3 },
  { id: 'rout-6', title: 'Behaviour Log', category: 'behaviour', completed: 1, total: 1 }
];

export const initialHabilitationActivities: HabilitationActivity[] = [
  { id: 'hab-1', title: 'Morning Balcony Walk', category: 'Physical', durationMinutes: 20, completed: true, scheduledTime: '07:30' },
  { id: 'hab-2', title: 'Gentle Chair Yoga & Stretch', category: 'Physical', durationMinutes: 15, completed: true, scheduledTime: '10:00' },
  { id: 'hab-3', title: 'Plant Watering & Gardening', category: 'Sensory', durationMinutes: 15, completed: false, scheduledTime: '16:30' },
  { id: 'hab-4', title: 'Evening Classical Music Session', category: 'Auditory', durationMinutes: 25, completed: false, scheduledTime: '19:00' }
];

export const initialCognitiveActivities: CognitiveActivity[] = [
  { id: 'cog-1', title: 'Family Photo Album Recognition', type: 'Reminiscence', durationMinutes: 15, completed: true, score: '9/10 Correct' },
  { id: 'cog-2', title: 'Simple Pattern Matching Game', type: 'Executive Function', durationMinutes: 10, completed: true, score: 'Completed' },
  { id: 'cog-3', title: 'Story Recall & Naming', type: 'Memory Retrieval', durationMinutes: 15, completed: false }
];

export const initialObservations: BehaviourObservation[] = [
  {
    id: 'obs-1',
    timestamp: '16:45 PM',
    type: 'confusion',
    note: 'Slight confusion regarding time of day after afternoon nap. Settled quickly after cup of herbal tea.',
    intensity: 'mild',
    caregiverActionTaken: 'Guided to living room window and showed evening sun.'
  }
];

export const initialAppointments: Appointment[] = [
  {
    id: 'app-1',
    title: 'Quarterly Cognitive Assessment',
    doctor: 'Dr. Arun Nair',
    specialty: 'Neurology',
    date: '28 Sep 2026',
    time: '10:30 AM',
    location: 'Apollo Healthcare Center, Clinic 304',
    status: 'upcoming'
  },
  {
    id: 'app-2',
    title: 'Routine Blood Panel & BP Check',
    doctor: 'Dr. Meera Sen',
    specialty: 'General Physician',
    date: '12 Oct 2026',
    time: '09:00 AM',
    location: 'Home Visit by Nurse',
    status: 'upcoming'
  }
];

export const initialLocation: LocationData = {
  status: 'at_home',
  address: '42 Jasmine Gardens, Green Glen Layout, Bengaluru',
  coordinates: { lat: 12.925, lng: 77.685 },
  safeZoneCenter: { lat: 12.925, lng: 77.685 },
  safeZoneRadiusMeters: 150,
  lastUpdated: '2 min ago',
  batteryLevel: 84
};

export const initialMovement: MovementData = {
  dailyKm: 3.1,
  steps: 4250,
  activityLevel: 'normal',
  lastMovementTime: '15 min ago'
};

export const initialSleep: SleepData = {
  durationHours: 7.33,
  quality: 'restful',
  sleepStart: '10:15 PM',
  sleepEnd: '05:35 AM',
  nightWakeups: 1
};

export const initialSafetyEvents: SafetyEvent[] = [
  {
    id: 'safe-1',
    timestamp: 'Yesterday 14:10',
    type: 'geofence_exit',
    severity: 'medium',
    resolved: true,
    description: 'Patient stepped beyond 150m boundary into front park lane. Escorted back safely by daughter.'
  }
];

export const initialFamiliarPeople: FamiliarPerson[] = [
  {
    id: 'fam-1',
    name: 'Anu Menon',
    relation: 'Daughter (Primary)',
    avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&q=80&w=150',
    lastRecognized: '5 min ago',
    status: 'frequent'
  },
  {
    id: 'fam-2',
    name: 'Suresh Menon',
    relation: 'Son',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=150',
    lastRecognized: 'Yesterday 18:30',
    status: 'frequent'
  },
  {
    id: 'fam-3',
    name: 'Lakshmi Amma',
    relation: 'Family Nurse / Care Assistant',
    avatar: 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&q=80&w=150',
    lastRecognized: 'Today 08:30',
    status: 'recent'
  }
];

export const initialRecognitionEvents: RecognitionEvent[] = [
  {
    id: 'rec-1',
    timestamp: '10:42 AM',
    personName: 'Anu Menon',
    relation: 'Daughter',
    confidenceScore: 98.4,
    cameraLocation: 'Living Room Smart Cam',
    status: 'recognized'
  }
];

export const initialPendant: PendantStatus = {
  connected: true,
  batteryLevel: 78,
  gpsStatus: 'available',
  speakerStatus: 'working',
  lastSync: '2 min ago',
  remindersActive: true
};

export const initialAIRecommendations: AIRecommendation[] = [
  {
    id: 'ai-rec-1',
    title: 'Short Balcony Gardening Activity',
    activityType: 'Sensory Habilitation',
    durationMinutes: 15,
    reason: 'Recent activity logs show that familiar outdoor plant care activities consistently lower afternoon restlessness.',
    recommendedTime: '16:30 PM (In 15 mins)',
    status: 'suggested',
    icon: 'Sprout'
  },
  {
    id: 'ai-rec-2',
    title: 'Listen to Carnatic Flute Melodies',
    activityType: 'Auditory Reminiscence',
    durationMinutes: 12,
    reason: 'Music listening logs indicate positive emotional response and enhanced verbal responsiveness during evening hours.',
    recommendedTime: '18:15 PM',
    status: 'suggested',
    icon: 'Music'
  },
  {
    id: 'ai-rec-3',
    title: 'Hydration Gentle Prompt',
    activityType: 'Daily Care',
    durationMinutes: 5,
    reason: 'Hydration tracking shows 5/7 glasses consumed. Offering warm water with lemon before 5 PM aligns with peak daily routines.',
    recommendedTime: '16:45 PM',
    status: 'suggested',
    icon: 'Droplets'
  }
];

export const initialAIInsights: AIInsight[] = [
  {
    id: 'ins-1',
    category: 'sleep',
    title: 'Stable Night Sleep Pattern',
    description: 'Raghavan averaged 7h 20m of continuous sleep this week with minimal nocturnal wandering.',
    timestamp: 'Today',
    metric: '7.3 hrs avg'
  },
  {
    id: 'ins-2',
    category: 'medication',
    title: 'High Morning Adherence',
    description: 'Morning medication adherence reached 98% over the past 30 days.',
    timestamp: 'This Week',
    metric: '98% adherence'
  }
];

export const initialTimelineEvents: TimelineEvent[] = [
  {
    id: 'tl-1',
    timestamp: '2026-09-25T16:45:00',
    timeDisplay: '16:45 PM',
    title: 'Caregiver Observation Logged',
    description: 'Slight confusion after afternoon nap. Guided to window; calm restored quickly.',
    category: 'behaviour',
    severity: 'info',
    iconName: 'Eye'
  },
  {
    id: 'tl-2',
    timestamp: '2026-09-25T13:00:00',
    timeDisplay: '13:00 PM',
    title: 'Lunch & Vitamin D Taken',
    description: 'Vitamin D3 (1000 IU) acknowledged by Anu Menon.',
    category: 'medication',
    severity: 'success',
    iconName: 'Pill'
  },
  {
    id: 'tl-3',
    timestamp: '2026-09-25T10:42:00',
    timeDisplay: '10:42 AM',
    title: 'Familiar Person Detected',
    description: 'Daughter (Anu Menon) recognized by Living Room Camera (98% confidence).',
    category: 'camera',
    severity: 'info',
    iconName: 'UserCheck'
  },
  {
    id: 'tl-4',
    timestamp: '2026-09-25T10:15:00',
    timeDisplay: '10:15 AM',
    title: 'Cognitive Activity Completed',
    description: 'Photo Album Recognition session completed with 9/10 score.',
    category: 'activities',
    severity: 'success',
    iconName: 'Brain'
  },
  {
    id: 'tl-5',
    timestamp: '2026-09-25T08:00:00',
    timeDisplay: '08:00 AM',
    title: 'Morning Medication Taken',
    description: 'Donepezil 5 mg taken after breakfast.',
    category: 'medication',
    severity: 'success',
    iconName: 'CheckCircle2'
  },
  {
    id: 'tl-6',
    timestamp: '2026-09-25T07:30:00',
    timeDisplay: '07:30 AM',
    title: 'Woke Up & Morning Walk',
    description: 'Raghavan woke up after 7h 20m of restful sleep.',
    category: 'care_plan',
    severity: 'info',
    iconName: 'Sun'
  }
];

export const initialReports: CareReport[] = [
  {
    id: 'rep-1',
    title: 'Weekly Comprehensive Care Report',
    type: 'weekly',
    generatedDate: '22 Sep 2026',
    period: '15 Sep - 21 Sep 2026',
    summary: 'Overall care adherence remained strong at 87%. Patient displayed stable mood and consistent sleep routines.',
    adherenceRate: 87,
    medicationRate: 91,
    cognitiveRate: 86,
    fileSize: '1.4 MB'
  },
  {
    id: 'rep-2',
    title: 'Doctor Consultation Briefing',
    type: 'doctor',
    generatedDate: '20 Sep 2026',
    period: 'Last 30 Days',
    summary: 'Clinical summary prepared for Dr. Arun Nair including medication adherence, cognitive scores, and incident logs.',
    adherenceRate: 89,
    medicationRate: 94,
    cognitiveRate: 83,
    fileSize: '2.1 MB'
  },
  {
    id: 'rep-3',
    title: 'Medication Adherence Log',
    type: 'medication',
    generatedDate: '15 Sep 2026',
    period: 'August 2026',
    summary: 'Full monthly audit log of prescribed dosages, timestamps, and caregiver acknowledgments.',
    adherenceRate: 91,
    medicationRate: 91,
    cognitiveRate: 85,
    fileSize: '890 KB'
  }
];

export const initialNotifications: NotificationItem[] = [
  {
    id: 'notif-1',
    title: 'Medication Reminder Pending',
    message: 'Evening Donepezil 5 mg is scheduled for 9:00 PM.',
    timestamp: '10 min ago',
    read: false,
    type: 'medication'
  },
  {
    id: 'notif-2',
    title: 'Pendant Synced Successfully',
    message: 'Battery level at 78%. GPS lock active.',
    timestamp: '1 hour ago',
    read: true,
    type: 'system'
  }
];
