export interface User {
  id: number; email: string; username: string; full_name: string | null;
  role: string; is_active: boolean; created_at: string;
}

export interface Camera {
  id: number; name: string; location: string | null; stream_url: string | null;
  status: string; latitude: number | null; longitude: number | null;
  is_active: boolean; created_at: string;
}

export interface Alert {
  id: number; camera_id: number; title: string; description: string | null;
  severity: string; status: string; anomaly_type: string | null;
  confidence: number; snapshot_url: string | null; assigned_to: number | null;
  created_at: string; resolved_at: string | null;
  camera: Camera | null;
}

export interface DashboardData {
  cameras: { total: number; online: number; offline: number };
  alerts: { total: number; open: number; high_severity: number };
  recent_alerts: { id: number; title: string; severity: string; status: string; camera_name: string | null; created_at: string }[];
}

export interface AuthResponse { access_token: string; token_type: string; }
