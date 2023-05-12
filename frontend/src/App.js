import "./App.css";
import Header from "./components/header/header";
import Search from "./components/search/search";
import FileUpload from "./components/file_upload";
import { Button, Alert, Container } from "react-bootstrap";
import drive from "./assets/image/drive.png";
import { useEffect, useState } from "react";
import Constant from "./constant";

function App() {
  const [status, setStatus] = useState(false);

  const getStatus = async () => {
    let response = await fetch(`${Constant.BASE_URL}/integrations/drive`, {
      credentials: "include",
    });
    let data = await response.json();
    setStatus(!!data.status);
  };

  const handlelogin = async () => {
    if (!status) {
      let response = await fetch(
        `${Constant.BASE_URL}/integrations/drive/authorize`,
        { credentials: "include" }
      );
      let data = await response.json();
      window.location.href = data.url;
    }
  };

  useEffect(() => {
    getStatus();
  }, []);

  return (
    <Container>
      <Header />
      <Button
        style={{
          background: "transparent",
          position: "fixed",
          bottom: "20px",
          right: "20px",
          border: "0px",
        }}
        onClick={handlelogin}
      >
        <img src={drive} width={60} />
      </Button>
      {status ? (
        <>
          <FileUpload />
          <Search />
        </>
      ) : (
        <Alert variant="primary">Click on Drive icon to login!</Alert>
      )}
    </Container>
  );
}

export default App;
