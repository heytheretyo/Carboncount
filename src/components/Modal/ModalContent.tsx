import { Checkbox } from "../Toggle/Toggle";
import "./ModalContent.css";

export function ModalContent() {
  return (
    <>
      <label htmlFor="cars">Your CPU model</label>
      <select name="cars" id="cars">
        <option value="volvo">Volvo</option>
        <option value="saab">Saab</option>
        <option value="mercedes">Mercedes</option>
        <option value="audi">Audi</option>
      </select>
      <label htmlFor="cars">Your GPU model</label>

      <select name="cars" id="cars">
        <option value="volvo">Volvo</option>
        <option value="saab">Saab</option>
        <option value="mercedes">Mercedes</option>
        <option value="audi">Audi</option>
      </select>

      <h4>this will ensure we calculate your power output accurately</h4>

      <div className="setting-panel">
        <h1>remind yourself to take a break</h1>
        <Checkbox />
      </div>
      <div className="setting-panel">
        <h1>notify carbon emmision at the end of the day (5:00pm)</h1>
        <Checkbox />
      </div>
      <div className="setting-panel">
        <h1>allow this app to run in the background</h1>
        <Checkbox />
      </div>
    </>
  );
}
