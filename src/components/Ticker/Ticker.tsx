/* global pywebview */

import * as React from "react";

import "./Ticker.sass";
import logo from "../../assets/logo.png";

interface Data {
  carbon_emmision: number;
  // Add other properties as needed
}

export default function Ticker() {
  const [ticker, setTicker] = React.useState("");
  const [uptimeValue, setUptime] = React.useState("");
  const [data, setData] = React.useState<any>({});

  React.useEffect(() => {
    window.addEventListener("pywebviewready", function () {
      if (!(window as any).pywebview.state) {
        (window as any).pywebview.state = {};
      }
      // Expose setTicker in order to call it from Python
      (window as any).pywebview.state.setTicker = setTicker;
    });
  }, []);

  React.useEffect(() => {
    const fetchUptime = async () => {
      try {
        const response = await (window as any).pywebview.api.get_data();
        setUptime(response.computer_uptime);
        setData(response);
      } catch (error) {
        console.error("Error fetching uptime:", error);
      }
    };

    setInterval(fetchUptime, 1000);
  }, []);

  return (
    <div className="ticker-container">
      <h1>carboncount</h1>
      <h1>
        your computer has been running for {uptimeValue[0]} day {uptimeValue[1]}
        hours {uptimeValue[2]} minutes {uptimeValue[3]} seconds
      </h1>

      <em>Thats around {data.carbon_emmision} kg in carbon emissions</em>

      <strong>{ticker}</strong>
    </div>
  );
}
