import {API_CONFIG, ApiError, clientApi} from './client.api';
import { IFileItem, IFileUploadRequest } from '../types/file.types';

export const fileApi = {
  async listFiles(): Promise<IFileItem[]> {
    return clientApi<IFileItem[]>('/files');
  },

  async uploadFile(request: IFileUploadRequest): Promise<IFileItem> {
    const formData = new FormData();
    formData.append('title', request.title);
    formData.append('file', request.file);

    return clientApi<IFileItem>('/files', {
      method: 'POST',
      body: formData,
      headers: {
        'Content-Type': undefined,
      },
    });
  },

  async updateFile(fileId: string, title: string): Promise<IFileItem> {
    return clientApi<IFileItem>(`/files/${fileId}`, {
      method: 'PATCH',
      body: JSON.stringify({ title }),
    });
  },

  async deleteFile(fileId: string): Promise<void> {
    return clientApi(`/files/${fileId}`, {
      method: 'DELETE',
    });
  },


};