import { clientApi } from './client.api';
import { IAlertItem } from '../types/alert.types';

export const alertApi = {
  async listAlerts(): Promise<IAlertItem[]> {
    return clientApi<IAlertItem[]>('/alerts');
  },

  async getAlertsByFile(fileId: string): Promise<IAlertItem[]> {
    return clientApi<IAlertItem[]>(`/files/${fileId}/alerts`);
  },
};