export const API_ENDPOINTS = {
  FILES: '/files',
  ALERTS: '/alerts',
  DOWNLOAD: (fileId: string) => `/files/${fileId}/download`,
} as const;

export const STATUS = {
  UPLOADED: 'uploaded',
  PROCESSING: 'processing',
  PROCESSED: 'processed',
  FAILED: 'failed',
} as const;

export const SCAN_STATUS = {
  CLEAN: 'clean',
  SUSPICIOUS: 'suspicious',
  PENDING: 'pending',
  FAILED: 'failed',
} as const;

export const ALERT_LEVELS = {
  CRITICAL: 'critical',
  WARNING: 'warning',
  INFO: 'info',
} as const;

export const STATUS_LABELS: Record<string, string> = {
  [STATUS.UPLOADED]: 'Загружен',
  [STATUS.PROCESSING]: 'Обработка...',
  [STATUS.PROCESSED]: 'Обработан',
  [STATUS.FAILED]: 'Ошибка',
  [SCAN_STATUS.CLEAN]: 'Безопасен',
  [SCAN_STATUS.SUSPICIOUS]: 'Подозрительный',
  [SCAN_STATUS.PENDING]: 'Ожидание',
  [SCAN_STATUS.FAILED]: 'Ошибка сканирования',
};

export const STATUS_VARIANTS: Record<string, string> = {
  [STATUS.UPLOADED]: 'secondary',
  [STATUS.PROCESSING]: 'warning',
  [STATUS.PROCESSED]: 'success',
  [STATUS.FAILED]: 'danger',
  [SCAN_STATUS.CLEAN]: 'success',
  [SCAN_STATUS.SUSPICIOUS]: 'warning',
  [SCAN_STATUS.PENDING]: 'secondary',
  [SCAN_STATUS.FAILED]: 'danger',
  [ALERT_LEVELS.CRITICAL]: 'danger',
  [ALERT_LEVELS.WARNING]: 'warning',
  [ALERT_LEVELS.INFO]: 'success',
};

export const DELAY_DEFAULT = 300;

export const kiloByteSize = 1024;
export const megaByteSize = kiloByteSize * 1024;