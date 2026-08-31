import {useCallback, useEffect, useState} from 'react';
import {IFileItem} from '../types/file.types';
import {fileApi} from '../services/file.api';
import {EToastType, useToast} from '@/shared/hooks/use-toast';

export function useFiles() {
  const [files, setFiles] = useState<IFileItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { showToast } = useToast();

  const loadFiles = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await fileApi.listFiles();
      setFiles(data);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load files';
      setError(message);
      showToast(EToastType.ERROR, message);
    } finally {
      setIsLoading(false);
    }
  };

  const uploadFile = async (title: string, file: File) => {
    try {
      const newFile = await fileApi.uploadFile({ title, file });
      setFiles(prev => [newFile, ...prev]);
      showToast(EToastType.SUCCESS, 'File uploaded successfully');
      return newFile;
    } catch (err) {
      showToast(EToastType.ERROR, err instanceof Error ? err.message : 'Failed to upload file');
      throw err;
    }
  };

  const deleteFile = async (fileId: string) => {
    try {
      await fileApi.deleteFile(fileId);
      setFiles(prev => prev.filter(f => f.id !== fileId));
      showToast(EToastType.SUCCESS, 'File deleted successfully');
    } catch (err) {
      showToast(EToastType.ERROR, err instanceof Error ? err.message : 'Failed to delete file');
      throw err;
    }
  };

  const updateFile = async (fileId: string, title: string) => {
    try {
      const updated = await fileApi.updateFile(fileId, title);
      setFiles(prev => prev.map(f => f.id === fileId ? updated : f));
      showToast(EToastType.SUCCESS, 'File updated successfully');
      return updated;
    } catch (err) {
      showToast(EToastType.ERROR, err instanceof Error ? err.message : 'Failed to update file');
      throw err;
    }
  };

  const refresh = useCallback(() => {
    loadFiles().then();
  }, [loadFiles]);

  useEffect(() => {
    loadFiles().then();
  }, []);

  return {
    files,
    isLoading,
    error,
    uploadFile,
    deleteFile,
    updateFile,
    refresh,
  };
}