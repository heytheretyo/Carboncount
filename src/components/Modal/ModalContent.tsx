import { useState, useEffect } from "react";
import { Checkbox } from "../Toggle/Toggle";
import "./ModalContent.css";
import { Button, Form } from "react-bootstrap";
import { options } from "../Charts/CarbonChart";
import { AsyncTypeahead, Typeahead } from "react-bootstrap-typeahead";
import { Option } from "react-bootstrap-typeahead/types/types";

export function ModalContent() {
  const [gpuData, setGpuData] = useState([]);
  const [cpuData, setCpuData] = useState([]);
  const [countryData, setCountryData] = useState([]);

  const [cpuSelection, setCpuSelection] = useState<any[]>([]);
  const [gpuSelection, setGpuSelection] = useState<any[]>([]);
  const [countrySelection, setCountrySelection] = useState<any[]>([]);

  const fetchGpuData = async (query: string) => {
    try {
      const response = await (window as any).pywebview.api.get_gpu_tdp_list(
        query
      );
      setGpuData(response);
    } catch (error) {
      console.error("Error fetching uptime:", error);
    }
  };

  useEffect(() => {
    const fetchCpuData = async () => {
      try {
        const response = await (window as any).pywebview.api.get_cpu_tdp_list();
        setCpuData(response);
      } catch (error) {
        console.error("Error fetching uptime:", error);
      }
    };
    fetchCpuData();
  }, []);

  useEffect(() => {
    const fetchCountryData = async () => {
      try {
        const response = await (window as any).pywebview.api.get_iso_list();
        setCountryData(response);
      } catch (error) {
        console.error("Error fetching uptime:", error);
      }
    };
    fetchCountryData();
  }, []);

  const saveSettings = async () => {
    const new_setting = {
      gpu_power:
        gpuSelection[0].tdp === "N/A" ? 90 : parseInt(gpuSelection[0].tdp, 10),
      cpu_power:
        cpuSelection[0].tdp === "N/A" ? 50 : parseInt(cpuSelection[0].tdp, 10),
      country:
        countrySelection[0].name === ""
          ? "United Kingdom"
          : countrySelection[0].name,
    };

    console.log(new_setting);

    await (window as any).pywebview.api.set_settings(new_setting);
  };

  return (
    <>
      <Form
        onSubmit={async (e) => {
          await saveSettings();
          e.preventDefault();
        }}
      >
        <Form.Group className="mb-4">
          <Form.Label>CPU Model</Form.Label>
          <Typeahead
            id="basic-typeahead-single"
            labelKey={(option: any) => option.name}
            options={cpuData}
            placeholder="Choose your CPU Model"
            onChange={(opt: any) => {
              setCpuSelection(opt);
            }}
            selected={cpuSelection}
          />
        </Form.Group>
        <Form.Group className="mb-4">
          <Form.Label>GPU Model</Form.Label>
          <AsyncTypeahead
            labelKey={(option: any) => option.name}
            options={gpuData}
            placeholder="Choose your GPU Model"
            onChange={(opt: any) => {
              setGpuSelection(opt);
            }}
            selected={gpuSelection}
            isLoading={false}
            onSearch={fetchGpuData}
          />
        </Form.Group>
        <Form.Group>
          <Form.Label>Your Country</Form.Label>
          <Typeahead
            id="basic-typeahead-single"
            labelKey={(option: any) => option.name}
            options={countryData}
            defaultSelected={["United Kingdom"]}
            placeholder="Choose your country"
            onChange={(opt: any) => {
              setCountrySelection(opt);
            }}
            selected={countrySelection}
          />
        </Form.Group>
        <Button variant="primary" type="submit" className="my-4">
          Save Settings
        </Button>
      </Form>

      <h4 style={{ fontSize: "1rem" }}>
        This will ensure we calculate your power output more accurately
      </h4>

      <h5 style={{ fontSize: ".9rem", fontStyle: "italic" }}>
        Currently, we are only able to use accurate minimum power draw for just
        the cpu, ram and gpu. For disk and display we are only using an average
        minimum power dray found from the internet
      </h5>
      <h5 style={{ fontSize: ".9rem", fontStyle: "bold", color: "green" }}>
        Your country will determine the carbon intensity which vary your carbon
        output geographically
      </h5>
    </>
  );
}
