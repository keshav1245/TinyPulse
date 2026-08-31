import { useState } from "react"
import { useNavigate, useParams, Link } from "react-router-dom"
import { 
    useSite,
    useDailyStas,
    useHealthChecks,
    useDowntimes,
    useTriggerHealthCheck,
    useDeleteSite,
} from "../hooks/useSites"

import StatusBadge from "../components/sites/StatusBadge"
import UptimeChart from "../components/site-detail/UptimeChart"
import HealthCheckList from "../components/site-detail/HealthCheckList"
import DowntimeList from "../components/site-detail/DowntimeList"

const DAY_OPTIONS = [7, 30, 90];

export default function SiteDetailPage(){
    
    const { siteId } = useParams<{ siteId: string }>();
    const navigate = useNavigate();
    const [days, setDays] = useState(7);

    const { data: site, isLoading: siteLoading} = useSite(siteId!);
    const { data: stats } = useDailyStas(siteId!, days);
    const { data: healthChecks } = useHealthChecks(siteId!, 100);
    const { data: downtimes } = useDowntimes(siteId!, 100);

    const triggerhealthCheck = useTriggerHealthCheck(siteId!);
    const deleteSite = useDeleteSite();

    if (siteLoading) return <p className="text-slate-500">Loading site...</p>
    if (!site) return <p className="text-red-600">Site not found!</p>
 
    const handleDelete = () => {
        if(window.confirm(`Delete "${site.name}"? This can't be undone from the UI.`)){
            deleteSite.mutate(site.site_id, { onSuccess: () => {navigate("/")}});
        }
    }

    return (
        <div className="space-y-6">
            <Link to="/" className="text-sm text-slate-500 hover:underline">
                &larr; Back to sites
            </Link>
        
            <div className="flex items-center justify-between">
                <div>
                    <div className="flex items-center gap-2">
                        <h1 className="text-2xl font-semibold text-slate-900">
                            {site.name}
                        </h1>
                        <StatusBadge status={site.latest_health_check?.site_stat} />
                    </div>
                    <p className="text-sm text-slate-500">{site.url}</p>
                </div>

                <div className="flex gap-2">
                    <button onClick={() => triggerhealthCheck.mutate()}
                        disabled={triggerhealthCheck.isPending}
                        className="rounded-md border border-slate-300 px-3 py-1.5 text-sm 
                        font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-50"
                        >
                            {triggerhealthCheck.isPending ? "Checking..." : "Check now"}
                    </button>
                    <button
                        onClick={handleDelete}
                        disabled={deleteSite.isPending}
                        className="rounded-md border border-red-200 px-3 py-1.5 text-sm font-medium text-red-600 hover:bg-red-50 disabled:opacity-50"
                    >
                        {deleteSite.isPending ? "Deleting..." : "Delete"}
                    </button>
                </div>

            </div>

            <div>
                <div className="mb-2 flex items-center justify-between">
                    <h2 className="text-lg font-medium text-slate-900">Uptime</h2>
                    <div className="flex gap-1">
                        {DAY_OPTIONS.map((d) => (
                            <button
                                key={d}
                                onClick={() => setDays(d)}
                                className={`rounded-md px-3 py-1 text-sm ${
                                    days === d ? "bg-slate-900 text-white" : "bg-slate-100 text-slate-600"
                                }`}
                            >
                                {d}d
                            </button>
                        ))}
                    </div>
                </div>
                <UptimeChart dailyStats={stats?.daily_stats ?? []}  />
            </div>

            <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
                <div>
                    <h2 className="mb-2 text-lg font-medium text-slate-900">Recent health checks</h2>
                    <HealthCheckList healthChecks={healthChecks ?? []} />
                </div>
                
                <div>
                    <h2 className="mb-2 text-lg font-mediumtext-slate-900">Downtime incidents</h2>
                    <DowntimeList downtimes={downtimes ?? []} />
                </div>

            </div>
        
        </div>
    );
}