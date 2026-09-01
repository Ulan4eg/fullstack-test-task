import {useCallback, useState} from 'react';
import {fileApi} from '../services/file.api';
import {EToastType, useToast} from '@/shared/hooks/use-toast';

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

      showToast(EToastType.SUCCESS, 'File uploaded successfully');
      options.onSuccess?.(result);

      return result;
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Upload failed');
      showToast(EToastType.ERROR, error.message);
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