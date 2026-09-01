import React, {useState, useRef} from 'react';
import {Modal, Form, Button} from 'react-bootstrap';
import {useFileUpload} from '../../hooks/use-file-upload';
import {ProgressBar} from 'react-bootstrap';
import {kiloByteSize} from "@/shared/constants";

interface IUploadModalProps {
  show: boolean;
  onHide: () => void;
  onUpload?: (title: string, file: File) => void;
}

export function UploadModal({show, onHide, onUpload}: IUploadModalProps) {
  const [title, setTitle] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const selectedFileSize = selectedFile ? Math.round(selectedFile.size / kiloByteSize) : 0;
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const {upload, isUploading, progress} = useFileUpload({
    onSuccess: (result) => {
      setTitle('');
      setSelectedFile(null);
      setError(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
      onUpload?.(result.title, result.file);
      onHide();
    },
    onError: (err) => {
      setError(err.message);
    },
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!title.trim()) {
      setError('Укажите название файла');
      return;
    }

    if (!selectedFile) {
      setError('Выберите файл');
      return;
    }

    await upload(title.trim(), selectedFile);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] || null;
    setSelectedFile(file);
    setError(null);
  };

  return (
    <Modal show={show} onHide={onHide} centered>
      <Form onSubmit={handleSubmit}>
        <Modal.Header closeButton>
          <Modal.Title>Добавить файл</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {error && (
            <div className="alert alert-danger">{error}</div>
          )}

          <Form.Group className="mb-3">
            <Form.Label>Название</Form.Label>
            <Form.Control
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Например, Договор с подрядчиком"
              disabled={isUploading}
            />
          </Form.Group>

          <Form.Group>
            <Form.Label>Файл</Form.Label>
            <Form.Control
              ref={fileInputRef}
              type="file"
              onChange={handleFileChange}
              disabled={isUploading}
            />
            {selectedFile && (
              <div className="mt-2 text-secondary small">
                Выбран: {selectedFile.name} ({selectedFileSize} KB)
              </div>
            )}
          </Form.Group>

          {isUploading && (
            <div className="mt-3">
              <ProgressBar
                now={progress}
                label={`${Math.round(progress)}%`}
                variant="primary"
              />
            </div>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={onHide} disabled={isUploading}>
            Отмена
          </Button>
          <Button type="submit" variant="primary" disabled={isUploading}>
            {isUploading ? 'Загрузка...' : 'Сохранить'}
          </Button>
        </Modal.Footer>
      </Form>
    </Modal>
  );
}