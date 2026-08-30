import Plot from "react-plotly.js";
import type { DailyStat } from "../../types/stats";

export default function UptimeChart({ dailyStats }: {
    dailyStats: DailyStat[]
}) {

    if (dailyStats.length === 0) {
        return <p className="text-sm text-slate-500">No data yet for this range.</p>
    }

    return (

        <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
            <Plot
                data={[
                    {
                        x: dailyStats.map((d) => d.date),
                        y: dailyStats.map((d) => d.uptime_percentage),
                        type: "scatter",
                        mode: "lines+markers",
                        line: { color: "#0f172a", width: 2 },
                        marker: { size: 4, color: "#0f172a" },
                        hovertemplate: "%{x}<br>Uptime: %{y:.1f}%<extra></extra>",
                    },
                ]}
                layout={{
                    autosize: true,
                    height: 256,
                    margin: { l: 40, r: 10, t: 10, b: 30 },
                    xaxis: { showgrid: false },
                    yaxis: { range: [0, 100], ticksuffix: "%", gridcolor: "#e2e8f0" },
                    plot_bgcolor: "white",
                    paper_bgcolor: "white",
                    font: { family: "inherit", size: 12 },
                }}
                config={{ displayModeBar: false, responsive: true }}
                style={{ width: "100%", height: "256px" }}
                useResizeHandler
            />
        </div>

    )

}