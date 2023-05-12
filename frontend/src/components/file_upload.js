import { useState } from "react";
import { Button, Form, Alert } from "react-bootstrap";
import Constant from "../constant";

export default function FileUpload() {
  const [file, setFile] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("file", file);

    fetch(`${Constant.BASE_URL}/integrations/drive/upload`, {
      method: "POST",
      body: formData,
    }).then((response) => {
      if (response.ok) {
        setSuccess(true);
        setFile(null);
        setTimeout(() => {
          setSuccess(false);
        }, 3000);
      } else {
        setSuccess(false);
      }
    });
  };

  return (
    <div>
      {success ? (
        <Alert variant="success">File uploaded successfully!</Alert>
      ) : (
        <></>
      )}
      <Form onSubmit={handleFormSubmit}>
        <Form.Group controlId="formFileMultiple" className="mb-3">
          <Form.Control type="file" onChange={handleFileChange} />
          <Button
            style={{ width: "100%" }}
            className="mt-3"
            variant="primary"
            type="submit"
          >
            Upload
          </Button>
        </Form.Group>
      </Form>
    </div>
  );
}
