export const validators = {
  // Проверка названия файла
  validateTitle(title: string): { valid: boolean; error?: string } {
    if (!title || !title.trim()) {
      return { valid: false, error: 'Название не может быть пустым' };
    }
    if (title.length > 255) {
      return { valid: false, error: 'Название не должно превышать 255 символов' };
    }
    if (/[<>:"/\\|?*]/.test(title)) {
      return { valid: false, error: 'Название содержит недопустимые символы' };
    }
    return { valid: true };
  },

  // Проверка размера файла
  validateFileSize(size: number, maxSizeMB: number = 100): { valid: boolean; error?: string } {
    const maxBytes = maxSizeMB * 1024 * 1024;
    if (size > maxBytes) {
      return {
        valid: false,
        error: `Файл слишком большой. Максимальный размер: ${maxSizeMB} MB`
      };
    }
    return { valid: true };
  },

  // Проверка типа файла
  validateFileType(
    mimeType: string,
    allowedTypes: string[] = [
      'application/pdf',
      'text/plain',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'image/jpeg',
      'image/png',
      'application/zip',
    ]
  ): { valid: boolean; error?: string } {
    if (!allowedTypes.includes(mimeType)) {
      return {
        valid: false,
        error: `Тип файла не поддерживается. Разрешены: ${allowedTypes.join(', ')}`
      };
    }
    return { valid: true };
  },

  // Проверка расширения файла
  validateFileExtension(
    filename: string,
    allowedExtensions: string[] = ['.pdf', '.txt', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.zip']
  ): { valid: boolean; error?: string } {
    const extension = filename.split('.').pop()?.toLowerCase();
    if (!extension || !allowedExtensions.includes(`.${extension}`)) {
      return {
        valid: false,
        error: `Расширение файла не поддерживается. Разрешены: ${allowedExtensions.join(', ')}`
      };
    }
    return { valid: true };
  },
};