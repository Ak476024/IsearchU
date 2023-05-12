import React, { useEffect, useState } from "react";
import { Form, InputGroup, Row } from "react-bootstrap";
import Constant from "../../constant";
import SearchItem from "./search_item";

export default function Search() {
  const [data, setData] = useState({});
  const [search, setSearch] = useState("");

  const fetchFiles = async () => {
    try {
      let response = await fetch(
        `${Constant.BASE_URL}/integrations/drive/files?q=${search}`,
        { credentials: "include" }
      );
      let data = await response.json();
      setData(data);
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {
    fetchFiles();
  }, []);

  return (
    <div>
      <Form
        onSubmit={(e) => {
          e.preventDefault();
          fetchFiles();
        }}
      >
        <InputGroup className="mb-3">
          <InputGroup.Text id="basic-addon1">search</InputGroup.Text>
          <Form.Control
            placeholder="keyword"
            aria-label="keyword"
            aria-describedby="basic-addon1"
            onChange={(e) => setSearch(e.target.value)}
          />
        </InputGroup>
      </Form>
      <Row>
        {data.files && data.files.map((file) => <SearchItem file={file} />)}
      </Row>
    </div>
  );
}
