interface IEmptyStateProps {
  message: string;
  icon?: string;
}

export function EmptyState({ message, icon = '📭' }: IEmptyStateProps) {
  return (
    <div className="text-center py-4 text-secondary">
      <div className="display-1 mb-3">{icon}</div>
      <p>{message}</p>
    </div>
  );
}