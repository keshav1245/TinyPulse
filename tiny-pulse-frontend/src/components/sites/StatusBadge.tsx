import type { SiteStatus } from "../../types/site";

const STYLES: Record<SiteStatus | "UNKNOWN", string> = {

    UP: "bg-emerald-100 text-emerald-700",
    DOWN: "bg-red-100 text-red-700",
    UNKNOWN: "bg-slate-100 text-slate-600"

}

export default function StatusBadge({ status }: {
    status: SiteStatus | null | undefined
}) {

    const key = status ?? "UNKNOWN";

    return (
        <span className={`inline-flex items-center rounded-full
        px-2.5 py-0.5 text-xs font-medium ${STYLES[key]}`}>
            {key}
        </span>
    );

}