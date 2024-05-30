/* global pywebview */

import * as React from "react";
import Chart from "chart.js/auto";
import {
  CategoryScale,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Title,
} from "chart.js";
import "./Ticker.css";
import "bootstrap/dist/css/bootstrap.min.css";
import logo from "../../assets/logo.png";
import { Checkbox } from "../Toggle/Toggle";
import {
  Button,
  Navbar,
  Container,
  ToggleButton,
  ToggleButtonGroup,
  Tooltip,
} from "react-bootstrap";
import { HeroStatistics } from "../Statistics/HeroStatistics";
import CarbonChart from "../Charts/CarbonChart";
import PowerChart from "../Charts/PowerChart";

interface Data {
  carbon_emmision: number;
}

Chart.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Legend
);

export default function Main() {
  const timelineType = ["daily", "monthly"];

  const [ticker, setTicker] = React.useState("");
  const [uptimeValue, setUptime] = React.useState("");
  const [data, setData] = React.useState<any>({});
  const [timeline, setTimeline] = React.useState<number>(0);

  const [powerData, setPowerData] = React.useState([]);
  const [carbonData, setCarbonData] = React.useState([]);

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
        console.log(response);
        setData(response);
      } catch (error) {
        console.error("Error fetching uptime:", error);
      }
    };

    setInterval(fetchUptime, 1000);
  }, []);

  const fetchHistorical = async (timeline: string) => {
    try {
      const response = await (window as any).pywebview.api.get_historical_data(
        timeline
      );
      setPowerData(response.power_data);
      setCarbonData(response.carbon_data);
    } catch (error) {
      console.error("Error fetching uptime:", error);
    }
  };

  const handleTimelineChange = () => {
    fetchHistorical(timelineType[timeline]);
  };

  return (
    <div className="ticker-container">
      <h1>welcome user</h1>
      <div className="hero-subtitle">
        <h2>Your computer has been running for:</h2>
        <p className="counter-text">
          {uptimeValue[0] || 0} day {uptimeValue[1] || 0} hours{" "}
          {uptimeValue[2] || 0} minutes {uptimeValue[3] || 0} seconds
        </p>

        <em>
          You are currently producing {data.carbon_emission || 0} kg in carbon
          emissions every second
        </em>
      </div>
      <HeroStatistics data={data} />
      {/* <div className="key-facts">
        <h1>key facts</h1>

        <ul>
          <li>
            Your a computer usage today is equivalent to riding 65km in an
            average car
          </li>
          <li>
            Your carbon neutral score is SEVERE you should be give your computer
            and nature a break!
          </li>
          <li>
            Your carbon emmision is 15% lower than yesterday, you are helping
            the planet :)
          </li>
        </ul>
      </div> */}
      <div className="mt-3">
        <ToggleButtonGroup
          type="radio"
          name="data_type"
          defaultValue={0}
          onChange={(v) => {
            setTimeline(v);
            handleTimelineChange();
          }}
          size="sm"
        >
          <ToggleButton id="tbg-radio-1" value={0}>
            Daily
          </ToggleButton>
          <ToggleButton id="tbg-radio-2" value={1}>
            Monthly
          </ToggleButton>
        </ToggleButtonGroup>
      </div>

      <CarbonChart carbonData={carbonData} type={timelineType[timeline]} />
      <PowerChart powerData={powerData} type={timelineType[timeline]} />
    </div>
  );
}
