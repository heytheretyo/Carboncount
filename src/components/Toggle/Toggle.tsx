import { useState } from "react";
import "./Toggle.css";

export function Checkbox() {
  const [check, setCheck] = useState(false);

  return (
    <label className="switch">
      <input type="checkbox" />
      <span className="slider round"></span>
    </label>
  );
}
