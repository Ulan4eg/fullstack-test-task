export const config = {
  api: {
    baseUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    timeout: 30000,
    retries: 3,
  },
  features: {
    fileUpload: {
      maxSize: 100 * 1024 * 1024, // 100 MB
      allowedTypes: [
        'application/pdf',
        'text/plain',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'image/jpeg',
        'image/png',
        'application/zip',
      ],
    },
  },
  ui: {
    toastDuration: 5000,
    pagination: {
      defaultPageSize: 50,
      pageSizes: [10, 25, 50, 100],
    },
  },
};