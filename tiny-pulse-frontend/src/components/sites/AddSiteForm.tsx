import React, { useState } from "react";
import { useCreateSite } from "../../hooks/useSites";

export default function AddSiteForm({ onDone }: {
    onDone : () => void
}){


    const [url, setUrl] = useState("")
    const [name, setName] = useState("")
    const [interval, setInterval] = useState(120)
    const createSite = useCreateSite()

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault()
        createSite.mutate(
            { url, name, interval, is_active: true}, 
            { onSuccess: onDone }
        )
    }

    return (
        <form onSubmit={handleSubmit} className="mb-6 space-y-3 rounded-lg border border-slate-200
        bg-white p-4 shadow-sm">

            <div>
                <label htmlFor="name" className="block text-sm font-medium text-slate-700">Site name</label>
                <input type="text" name="name" id="name" 
                    value={name} onChange={(e) => setName(e.target.value)}
                    required
                    className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
                    placeholder="My API Site"
                />
            </div>
            <div>
                <label htmlFor="url" className="block text-sm font-medium text-slate-700">URL</label>
                <input type="url" name="url" id="url" 
                    value={url} onChange={(e) => setUrl(e.target.value)}
                    required
                    className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
                    placeholder="https://example.com"
                />
            </div>
            <div>
                <label htmlFor="interval" className="block text-sm font-medium text-slate-700">Check Interval (seconds)</label>
                <input type="number" name="interval" id="interval" 
                    value={interval} onChange={(e) => setInterval(Number(e.target.value))}
                    required
                    min={10}
                    className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2 text-sm"
                />
            </div>
            {
                createSite.isError && <p className="text-sm text-red-600">
                    {(createSite.error as Error).message}
                </p>
            }
            <div className="flex gap-2">
                <button
                    type="submit"
                    disabled={createSite.isPending}
                    className="rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white
                    hover:bg-slate-700 disabled:opacity-50"
                >
                    {createSite.isPending ? "Registering Site..." : "Register Site"}
                </button>
                <button type="button" onClick={onDone} className="rounded-md px-4 py-2 text-sm font-medium text-slate-600">
                    Cancel
                </button>
            </div>
        </form>
    )


}