import { Link } from "react-router-dom";
import StatusBadge from "./StatusBadge";
import type { SiteResponse } from "../../types/site";
import { useTriggerHealthCheck } from "../../hooks/useSites";

export default function SiteCard({ site }: {
    site: SiteResponse
}){

    const triggerHealthCheck = useTriggerHealthCheck(site.site_id);

    return (
        <div className="flex items-center justify-between rounded-lg
        border border-slate-200 bg-white p-4 shadow-sm">
            <div>
                <div className="flex items-center gap-2">
                    <Link to={`/sites/${site.site_id}`} 
                    className="font-medium text-slate-900 hover:underline"
                    >
                        {site.name}
                    </Link>
                    <StatusBadge status={site.latest_health_check?.site_stat} />
                </div>
                <p className="mt-1 text-sm text-slate-500">{site.url}</p>
                <p className="mt-1 text-xs text-slate-400">Checks every {site.interval}</p>
            </div>
            <button onClick={() => triggerHealthCheck.mutate()}
                disabled={triggerHealthCheck.isPending}
                className="rounded-md border border-slate-300 px-3 py-1.5 text-sm
                font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-50"
                >
                {triggerHealthCheck.isPending ? "Checking..." : "Check now"}
            </button>
        </div>
    )


}