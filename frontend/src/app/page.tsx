'use client';

import {useState} from 'react';
import {Alert, Badge, Button, Card, Col, Container, Row} from 'react-bootstrap';
import {useFiles} from '@/files/hooks/use-files';
import {useAlerts} from '@/files/hooks/use-alerts';
import {FileTable} from '@/files/components/file-list/file-table';
import {AlertTable} from '@/files/components/alert-list/alert-table';
import {UploadModal} from '@/files/components/file-upload/upload-modal';
import {LoadingSpinner} from '@/shared/components/loading-spinner';

export default function Page() {
  const [showUploadModal, setShowUploadModal] = useState(false);
  const {
    files,
    isLoading: filesLoading,
    error,
    uploadFile,
    refresh,
  } = useFiles();
  const {alerts, isLoading: alertsLoading} = useAlerts();

  const handleUpload = async (title: string, file: File) => {
    await uploadFile(title, file);
    setShowUploadModal(false);
  };

  const handleHideModal = () => {
    setShowUploadModal(false);
  }

  const handleShowUploadModal = () => {
    setShowUploadModal(true);
  }

  return (
    <Container fluid className="py-4 px-4 bg-light min-vh-100">
      <Row className="justify-content-center">
        <Col xxl={10} xl={11}>
          {/* Header unit */}
          <Card className="shadow-sm border-0 mb-4">
            <Card.Body className="p-4">
              <div className="d-flex justify-content-between align-items-start gap-3 flex-wrap">
                <div>
                  <h1 className="h3 mb-2">Управление файлами</h1>
                  <p className="text-secondary mb-0">
                    Загрузка файлов, просмотр статусов обработки и ленты алертов.
                  </p>
                </div>
                <div className="d-flex gap-2">
                  <Button variant="outline-secondary" onClick={refresh}>
                    Обновить
                  </Button>
                  <Button variant="primary" onClick={handleShowUploadModal}>
                    Добавить файл
                  </Button>
                </div>
              </div>
            </Card.Body>
          </Card>

          {/* Error unit */}
          {error && (
            <Alert variant="danger" className="shadow-sm">
              {error}
            </Alert>
          )}

          {/* Files unit */}
          <Card className="shadow-sm border-0 mb-4">
            <Card.Header className="bg-white border-0 pt-4 px-4">
              <div className="d-flex justify-content-between align-items-center">
                <h2 className="h5 mb-0">Файлы</h2>
                <Badge bg="secondary">{files.length}</Badge>
              </div>
            </Card.Header>
            <Card.Body className="px-4 pb-4">
              {filesLoading ? (
                <LoadingSpinner/>
              ) : (
                <FileTable files={files}/>
              )}
            </Card.Body>
          </Card>

          {/* Alerts unit */}
          <Card className="shadow-sm border-0">
            <Card.Header className="bg-white border-0 pt-4 px-4">
              <div className="d-flex justify-content-between align-items-center">
                <h2 className="h5 mb-0">Алерты</h2>
                <Badge bg="secondary">{alerts.length}</Badge>
              </div>
            </Card.Header>
            <Card.Body className="px-4 pb-4">
              {alertsLoading ? (
                <LoadingSpinner/>
              ) : (
                <AlertTable alerts={alerts}/>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <UploadModal
        show={showUploadModal}
        onHide={handleHideModal}
        onUpload={handleUpload}
      />
    </Container>
  );
}