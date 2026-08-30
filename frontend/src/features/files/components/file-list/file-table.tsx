import { Table } from 'react-bootstrap';
import { IFileItem } from '../../types/file.types';
import { FileRow } from './file-row';
import { EmptyState } from '@/shared/components/EmptyState';

interface FileTableProps {
  files: IFileItem[];
  onDelete?: (id: string) => void;
  onUpdate?: (id: string, title: string) => void;
}

export function FileTable({ files, onDelete, onUpdate }: FileTableProps) {
  if (files.length === 0) {
    return <EmptyState message="Файлы пока не загружены" />;
  }

  return (
    <div className="table-responsive">
      <Table hover bordered className="align-middle mb-0">
        <thead className="table-light">
        <tr>
          <th>Название</th>
          <th>Файл</th>
          <th>MIME</th>
          <th>Размер</th>
          <th>Статус</th>
          <th>Проверка</th>
          <th>Создан</th>
          <th>Действия</th>
        </tr>
        </thead>
        <tbody>
        {files.map((file) => (
          <FileRow
            key={file.id}
            file={file}
            onDelete={onDelete}
            onUpdate={onUpdate}
          />
        ))}
        </tbody>
      </Table>
    </div>
  );
}