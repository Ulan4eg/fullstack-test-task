import { useState } from 'react';
import { Badge, Button, Form, Modal } from 'react-bootstrap';
import { IFileItem } from '../../types/file.types';
import { StatusBadge } from '../file-status/status-badge';
import { formatters } from '../../utils/formatters';

interface FileRowProps {
  file: IFileItem;
  onDelete?: (id: string) => void;
  onUpdate?: (id: string, title: string) => void;
}

export function FileRow({ file, onDelete, onUpdate }: FileRowProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(file.title);

  const handleUpdate = () => {
    if (onUpdate && editTitle.trim() && editTitle !== file.title) {
      onUpdate(file.id, editTitle.trim());
    }
    setIsEditing(false);
  };

  const handleDownload = () => {
    window.open(`http://localhost:8000/files/${file.id}/download`, '_blank');
  };

  return (
    <tr>
      <td>
        <div className="fw-semibold">{file.title}</div>
        <div className="small text-secondary">{file.id}</div>
      </td>
      <td>{file.original_name}</td>
      <td>{file.mime_type}</td>
      <td>{formatters.fileSize(file.size)}</td>
      <td>
        <StatusBadge status={file.processing_status} />
      </td>
      <td>
        <div className="d-flex flex-column gap-1">
          <StatusBadge
            status={file.scan_status || 'pending'}
            requiresAttention={file.requires_attention}
          />
          <span className="small text-secondary">
            {file.scan_details || 'Ожидает обработки'}
          </span>
        </div>
      </td>
      <td>{formatters.date(file.created_at)}</td>
      <td className="text-nowrap">
        <div className="d-flex gap-1">
          <Button
            variant="outline-primary"
            size="sm"
            onClick={handleDownload}
          >
            Скачать
          </Button>
          <Button
            variant="outline-secondary"
            size="sm"
            onClick={() => setIsEditing(true)}
          >
            ✏️
          </Button>
          {onDelete && (
            <Button
              variant="outline-danger"
              size="sm"
              onClick={() => onDelete(file.id)}
            >
              🗑️
            </Button>
          )}
        </div>
      </td>

      {/* Modal для редактирования */}
      <Modal show={isEditing} onHide={() => setIsEditing(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>Редактировать название</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form.Group>
            <Form.Label>Название файла</Form.Label>
            <Form.Control
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              placeholder="Введите новое название"
            />
          </Form.Group>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setIsEditing(false)}>
            Отмена
          </Button>
          <Button variant="primary" onClick={handleUpdate}>
            Сохранить
          </Button>
        </Modal.Footer>
      </Modal>
    </tr>
  );
}