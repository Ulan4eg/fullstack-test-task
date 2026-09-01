import { Badge } from 'react-bootstrap';
import { IAlertItem } from '../../types/alert.types';
import { formatters } from '../../utils/formatters';

interface AlertRowProps extends IAlertItem {
}

const LEVEL_VARIANTS: Record<string, string> = {
  critical: 'danger',
  warning: 'warning',
  info: 'success',
};

export function AlertRow({ level, file_id, message, created_at, id }: AlertRowProps) {
  const variant = LEVEL_VARIANTS[level] || 'secondary';

  return (
    <tr>
      <td>{id}</td>
      <td className="small">{file_id}</td>
      <td>
        <Badge bg={variant}>{level}</Badge>
      </td>
      <td>{message}</td>
      <td>{formatters.date(created_at)}</td>
    </tr>
  );
}