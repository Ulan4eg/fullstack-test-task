import { Spinner } from 'react-bootstrap';

interface ILoadingSpinnerProps {
  message?: string;
}

const LOADING_MESSAGE_DEFAULT = 'Загрузка...';

export function LoadingSpinner({ message = LOADING_MESSAGE_DEFAULT }: ILoadingSpinnerProps) {
  return (
    <div className="d-flex flex-column align-items-center justify-content-center py-5">
      <Spinner animation="border" variant="primary" />
      <p className="mt-3 text-secondary">{message}</p>
    </div>
  );
}