import type { HealthCheckResponse } from "../../types/health-check";
import StatusBadge from "../sites/StatusBadge";


export default function HealthCheckList({ healthChecks }: {
    healthChecks: HealthCheckResponse[]
}){

    if (healthChecks.length === 0){
        return <p className="text-sm text-slate-500">
            No health checks recorded yet.
        </p>
    }

    const sorted = [...healthChecks].reverse();

    return (
        <ul className="max-h-96 divide-y divide-slate-200 overflow-y-auto rounded-lg border border-slate-200
        bg-white shadow-sm">
            {
                sorted.map((hc) => (
                    <li key={hc.id} className="flex items-center justify-between px-4 py-2 text-sm">
                        <div className="flex items-center gap-2">
                            <StatusBadge status={hc.site_stat} />
                            <span className="text-slate-600">{hc.status_code ?? "-"}</span>
                        </div>
                        <span className="text-slate-400">{new Date(hc.date_created).toLocaleString()}</span>
                    </li>
                ))
            }
        </ul>
    )

}