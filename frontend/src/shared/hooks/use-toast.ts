import { useCallback } from 'react';
import {DELAY_DEFAULT} from "@/shared/constants";

export enum EToastType {
  SUCCESS = 'success',
  ERROR = 'error',
  WARNING = 'warning',
  INFO = 'info',
}

interface IToast {
  id: string;
  type: EToastType;
  message: string;
  duration?: number;
}

let toastContainer: HTMLDivElement | null = null;
const TOAST_DURATION_DEFAULT = 5000;

export function useToast() {
  const showToast = useCallback((type: EToastType, message: string, duration = TOAST_DURATION_DEFAULT) => {
    if (!toastContainer) {
      toastContainer = document.createElement('div');
      toastContainer.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        display: flex;
        flex-direction: column;
        gap: 8px;
        max-width: 400px;
      `;
      document.body.appendChild(toastContainer);
    }

    const toast = document.createElement('div');
    const colors: Record<EToastType, string> = {
      success: '#28a745',
      error: '#dc3545',
      warning: '#ffc107',
      info: '#17a2b8',
    };

    toast.style.cssText = `
      padding: 12px 20px;
      background: ${colors[type]};
      color: white;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      animation: slideIn 0.3s ease;
      font-size: 14px;
    `;

    toast.textContent = message;
    toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.style.animation = 'slideOut 0.3s ease';
      setTimeout(() => {
        toast.remove();
        if (toastContainer && toastContainer.children.length === 0) {
          toastContainer.remove();
          toastContainer = null;
        }
      }, DELAY_DEFAULT);
    }, duration);
  }, []);

  if (typeof document !== 'undefined') {
    const style = document.createElement('style');
    style.textContent = `
      @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
      }
      @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
      }
    `;
    document.head.appendChild(style);
  }

  return { showToast };
}