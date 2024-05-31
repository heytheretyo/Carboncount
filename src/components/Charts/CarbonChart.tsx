import React from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Line } from "react-chartjs-2";
import { MonthlyLabels, DailyLabels } from "./Labels";

export const options = {
  plugins: {
    legend: {
      position: "top" as const,
    },
    title: {
      display: true,
      text: "Carbon Usage",
    },
  },
};

export default function CarbonChart({
  carbonData,
  type,
}: {
  carbonData?: Record<string, any>[];
  type: string;
}) {
  const data = {
    labels: type === "monthly" ? DailyLabels : MonthlyLabels,
    datasets: [
      {
        label: "CO2e (kg)",
        data: carbonData?.map((v) => v.total_carbon_emission) || [],
        borderColor: "rgb(255, 99, 132)",
        backgroundColor: "rgba(255, 99, 132, 0.5)",
      },
    ],
  };
  return (
    <div>
      <div
        style={{
          display: "flex",
          justifyContent: "center",
        }}
        className="my-5"
      >
        <Line options={options} data={data} />
      </div>
    </div>
  );
}
