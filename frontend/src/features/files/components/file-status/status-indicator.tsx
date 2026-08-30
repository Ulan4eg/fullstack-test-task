import { Spinner } from 'react-bootstrap';

interface IStatusIndicatorProps {
  status: string;
  size?: 'sm' | 'md' | 'lg';
}

export function StatusIndicator({ status, size = 'md' }: IStatusIndicatorProps) {
  const getIndicator = () => {
    switch (status) {
      case 'processing':
        return <Spinner animation="border" size={size} variant="warning" />;
      case 'uploaded':
        return <span className="text-secondary">⏳</span>;
      case 'processed':
        return <span className="text-success">✅</span>;
      case 'failed':
        return <span className="text-danger">❌</span>;
      default:
        return <span className="text-secondary">●</span>;
    }
  };

  return <span className="d-inline-block">{getIndicator()}</span>;
}