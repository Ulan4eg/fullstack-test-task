export type IAlertLevel = 'critical' | 'warning' | 'info';

export interface IAlertItem {
  id: number;
  file_id: string;
  level: IAlertLevel;
  message: string;
  created_at: string;
}

