import { useState, useEffect } from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Modal from "react-bootstrap/Modal";

export default function ModalBox({ show, setShow }: any) {
  const [gpuData, setGpuData] = useState([]);
  const [cpuData, setCpuData] = useState([]);

  useEffect(() => {
    const fetchGpuData = async () => {
      try {
        const response = await (window as any).pywebview.api.get_gpu_tdp_list();
        setGpuData(response.computer_uptime);
      } catch (error) {
        console.error("Error fetching uptime:", error);
      }
    };
    fetchGpuData();
  }, []);

  useEffect(() => {
    const fetchCpuData = async () => {
      try {
        const response = await (window as any).pywebview.api.get_cpu_tdp_list();
        setCpuData(response.computer_uptime);
      } catch (error) {
        console.error("Error fetching uptime:", error);
      }
    };
    fetchCpuData();
  }, []);

  return (
    <>
      <Modal show={show} onHide={setShow(!show)}>
        <Modal.Header closeButton>
          <Modal.Title>Settings</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Select aria-label="Default select example">
              <option>Select your cpu model</option>
              {cpuData.map((data) => {
                return (
                  <>
                    <h1>{data}</h1>
                  </>
                );
              })}
            </Form.Select>

            <Form.Select aria-label="Default select example">
              <option>Select your gpu model</option>
              <option value="1">One</option>
              <option value="2">Two</option>
              <option value="3">Three</option>
            </Form.Select>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={setShow(!show)}>
            Close
          </Button>
          <Button variant="primary" onClick={setShow(!show)}>
            Save Changes
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}
