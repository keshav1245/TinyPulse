import { Link } from "react-router-dom";


export default function Navbar(){
    return (
        <header className="border-b border-slate-200 bg-white">
            <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-4">
                <Link to="/" className="text-lg font-semibold text-slate-900 ">
                    TinyPulse
                </Link>
                <span className="text-sm text-slate-500">Uptime Monitoring</span>
            </div>
        </header>
    )
}