export function HeroStatistics() {
  const currentCarbonOutput = 0;
  const weeklyCarbonOutput = 0;
  const severity = "NORMAL";

  return (
    <>
      <div className="data_list">
        <div>
          <h1 className="data_content_header">total emmited today</h1>

          <p className="counter-text">
            {currentCarbonOutput || 0} kg of carbon
          </p>
        </div>

        <div>
          <h1 className="data_content_header">weekly emmision</h1>

          <p className="counter-text">{weeklyCarbonOutput || 0} kg of carbon</p>
        </div>

        <div>
          <h1 className="data_content_header">carbon neutral score</h1>
          <p className="counter-text">{severity || "NORMAL"}</p>
          {/* <p>
          Your carbon neutral score falls on the{" "}
          <span style={{ color: "red" }}>SEVERE</span> category, please limit
          your computer usage to safe the environment!
        </p> */}
        </div>
      </div>
    </>
  );
}
