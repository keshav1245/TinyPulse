import { Routes, Route } from "react-router-dom";
import Layout from "./components/layout/Layout"
import DashboardPage from "./pages/DashboardPage"
import SiteDetailPage from  "./pages/SiteDetailPage"
import NotFoundPage from "./pages/NotFoundPage"

export default function App(){
	return (
		<Layout>
			<Routes>
				<Route path="/" element={<DashboardPage />} />
				<Route path="/sites/:siteId" element={<SiteDetailPage />} />
				<Route path="/*" element={<NotFoundPage />} />
			</Routes>
		</Layout>
	)
}