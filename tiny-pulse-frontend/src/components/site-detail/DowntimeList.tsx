import type { DowntimeResponse } from "../../types/downtime";

function formatDuration( seconds: number | null){
    if (seconds == null) return "ongoing";
    const minutes = Math.round(seconds / 60);
    return minutes < 1 ? `${Math.round(seconds)}s` : `${minutes}m`
}

export default function DowntimeList({ downtimes } : {
    downtimes: DowntimeResponse[]
}){


    if(downtimes.length === 0){
        return <p className="text-sm text-slate-500">No downtime recorded.</p>
    }

    return (
        <ul className="divide-y divide-slate-200 rounded-lg border border-slate-200
        bg-white shadow-sm">

            {downtimes.map((dt) => (
                <li key={dt.id} className="flex items-center justify-between px-4 py-2 text-sm">
                    <span className="text-slate-600">{new Date(dt.start_time).toLocaleString()}</span>
                    <span className="font-medium text-red-600">{formatDuration(dt.duration_seconds)}</span>
                </li>
            ))}

        </ul>
    )

}