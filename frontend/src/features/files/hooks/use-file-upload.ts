import { useState, useCallback } from 'react';
import { fileApi } from '../services/file.api';
import { useToast } from '@/shared/hooks/useToast';

interface UseFileUploadOptions {
  onSuccess?: (file: any) => void;
  onError?: (error: Error) => void;
}

export function useFileUpload(options: UseFileUploadOptions = {}) {
  const [isUploading, setIsUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const { showToast } = useToast();

  const upload = useCallback(async (title: string, file: File) => {
    setIsUploading(true);
    setProgress(0);

    try {
      // Симуляция прогресса
      const progressInterval = setInterval(() => {
        setProgress(prev => {
          const next = prev + Math.random() * 10;
          return next > 90 ? 90 : next;
        });
      }, 200);

      const result = await fileApi.uploadFile({ title, file });

      clearInterval(progressInterval);
      setProgress(100);

      showToast('success', 'File uploaded successfully');
      options.onSuccess?.(result);

      return result;
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Upload failed');
      showToast('error', error.message);
      options.onError?.(error);
      throw error;
    } finally {
      setIsUploading(false);
      setTimeout(() => setProgress(0), 1000);
    }
  }, [showToast, options]);

  return {
    upload,
    isUploading,
    progress,
  };
}