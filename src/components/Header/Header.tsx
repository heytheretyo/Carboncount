import * as React from "react";

import "./Header.css";
import logo from "../../assets/logo.png";
import ModalBox from "../Modal/ModalBox";
import { Modal, Form, Button } from "react-bootstrap";
import ToggleButton from "react-bootstrap/ToggleButton";
import { ModalContent } from "../Modal/ModalContent";

export default function Header() {
  const [isOpen, setIsOpen] = React.useState(false);

  return (
    <div className="header-container">
      <img className="logo" src={logo} alt="pywebview" />
      <h2>carboncount*</h2>

      <div className="links">
        <h2 className="setting" onClick={() => setIsOpen(true)}>
          settings
        </h2>
      </div>

      <Modal show={isOpen} onHide={() => setIsOpen(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>Settings</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <ModalContent />
        </Modal.Body>
        <Modal.Footer>
          <Button variant="primary" onClick={() => setIsOpen(false)}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}
