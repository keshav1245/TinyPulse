import { Link } from "react-router-dom"

export default function NotFoundPage(){
    return (
        <div className="text-center">
            <h1 className="text-2xl font-semibold text-slate-900">404</h1>
            <p className="mt-2 text-slate-500">Page not found.</p>
            <Link to="/" className="mt-4 inline-block text-sm text-slate-700 underline">
                Back to dashboard.
            </Link>
        </div>
    )
}