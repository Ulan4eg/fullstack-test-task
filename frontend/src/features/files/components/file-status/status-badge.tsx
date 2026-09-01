import { Badge } from 'react-bootstrap';

interface IStatusBadgeProps {
  status: string;
  requiresAttention?: boolean;
}

const STATUS_VARIANTS: Record<string, string> = {
  uploaded: 'secondary',
  processing: 'warning',
  processed: 'success',
  failed: 'danger',
  clean: 'success',
  suspicious: 'warning',
  pending: 'secondary',
  'null': 'secondary',
};

const STATUS_LABELS: Record<string, string> = {
  uploaded: 'Загружен',
  processing: 'Обработка...',
  processed: 'Обработан',
  failed: 'Ошибка',
  clean: 'Безопасен',
  suspicious: 'Подозрительный',
  pending: 'Ожидание',
};

export function StatusBadge({ status, requiresAttention }: IStatusBadgeProps) {
  const variant = STATUS_VARIANTS[status] || 'secondary';
  const label = STATUS_LABELS[status] || status;

  if (requiresAttention) {
    return (
      <Badge bg="warning" className="d-flex align-items-center gap-1">
        <span>⚠️</span> {label}
      </Badge>
    );
  }

  return <Badge bg={variant}>{label}</Badge>;
}