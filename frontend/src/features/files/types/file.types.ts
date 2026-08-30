export type IProcessingStatus = 'uploaded' | 'processing' | 'processed' | 'failed';
export type IScanStatus = 'clean' | 'suspicious' | 'pending' | 'failed' | null;

export interface IFileItem {
  id: string;
  title: string;
  original_name: string;
  mime_type: string;
  size: number;
  processing_status: IProcessingStatus;
  scan_status: IScanStatus;
  scan_details: string | null;
  metadata_json: Record<string, any> | null;
  requires_attention: boolean;
  created_at: string;
  updated_at: string;
}

export interface IFileUploadRequest {
  title: string;
  file: File;
}

