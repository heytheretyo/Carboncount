import React, { useEffect } from "react";
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

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export const options = {
  plugins: {
    legend: {
      position: "top" as const,
    },
    title: {
      display: true,
      text: "Power Usage",
    },
  },
};

const data = {
  responsive: true,
  labels: MonthlyLabels,
  datasets: [
    {
      label: "Watts (W)",
      data: [12, 23, 2, 323, 1, 32, 1],
      borderColor: "rgb(255, 99, 132)",
      backgroundColor: "rgba(255, 99, 132, 0.5)",
    },
  ],
};

export default function PowerChart({
  powerData,
  type,
}: {
  powerData?: Record<string, any>[];
  type: string;
}) {
  const data = {
    responsive: true,
    labels: type === "monthly" ? MonthlyLabels : DailyLabels,
    datasets: [
      {
        label: "Watts (W)",
        data: powerData?.map((v) => v.total_power_consumption) || [],
        borderColor: "rgb(255, 99, 132)",
        backgroundColor: "rgba(255, 99, 132, 0.5)",
      },
    ],
  };

  return (
    <>
      <div
        style={{
          display: "flex",
          paddingRight: "30rem",
          paddingLeft: "30rem",
          justifyContent: "center",
        }}
        className="mb-5"
      >
        <Line options={options} data={data} />
      </div>
    </>
  );
}
