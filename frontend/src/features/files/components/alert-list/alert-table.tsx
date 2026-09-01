import {Table} from 'react-bootstrap';
import {IAlertItem} from '../../types/alert.types';
import {AlertRow} from './alert-row';
import {EmptyState} from '@/shared/components/empty-state';

interface AlertTableProps {
  alerts: IAlertItem[];
}

export function AlertTable({alerts}: AlertTableProps) {
  if (alerts.length === 0) {
    return <EmptyState message="Алертов пока нет"/>;
  }

  return (
    <div className="table-responsive">
      <Table hover bordered className="align-middle mb-0">
        <thead className="table-light">
        <tr>
          <th>ID</th>
          <th>File ID</th>
          <th>Уровень</th>
          <th>Сообщение</th>
          <th>Создан</th>
        </tr>
        </thead>
        <tbody>
        {alerts.map((alert) => (
          <AlertRow key={alert.id} {...alert} />
        ))}
        </tbody>
      </Table>
    </div>
  );
}