import React from "react";
import { Card, Col, Button } from "react-bootstrap";

export default function SearchItem({ file }) {
  return (
    file.webContentLink && (
      <Col>
        <Card
          style={{
            width: "18rem",
            margin: "10px 0px",
            height: "220px",
          }}
        >
          <Card.Body>
            <Card.Title style={{ wordBreak: "break-all" }}>
              <img src={file.iconLink} /> {file.name.toLowerCase()}
            </Card.Title>
          </Card.Body>
          <Card.Footer>
            <Button
              style={{ width: "100%" }}
              href={file.webContentLink}
              variant="primary"
            >
              Download
            </Button>
          </Card.Footer>
        </Card>
      </Col>
    )
  );
}
