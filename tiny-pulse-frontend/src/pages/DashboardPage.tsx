import { useState } from "react"
import { useSites } from "../hooks/useSites"
import SiteCard from "../components/sites/SiteCard"
import AddSiteForm from "../components/sites/AddSiteForm"


export default function DashboardPage(){
    
    const { data: sites, isLoading, isError, error } = useSites();
    const [showForm, setShowForm] = useState(false);
    
    
    return (
        <div>
            <div className="mb-6 flex items-center justify-between">
                <h1 className="text-2xl font-semibold text-slate-900">Sites</h1>

                <button onClick={() => setShowForm((v) => !v)}
                    className="rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white
                    hover:bg-slate-700"
                    >
                        {showForm ? "Close" : "+ Register Site"}
                </button>
            </div>
            {showForm && <AddSiteForm onDone={() => setShowForm(false)} />}
            {isLoading && <p className="text-slate-500">Loading sites...</p> }
            {
                sites && sites.length === 0 && (
                    <p className="text-slate-500">No sites yet; Register on to start monitoring!</p>
                )
            }

            <div className="space-y-3">
                {
                    sites?.map((site) => (
                        <SiteCard key={site.site_id} site={site} />
                    ))
                }
            </div>
        </div>
    )
}