import { apiClient } from "./client";
import type { SiteCreate, SiteResponse } from "../types/site";
import type { HealthCheckResponse } from "../types/health-check";
import type { DowntimeResponse } from "../types/downtime";
import type { SiteDailyStatsResponse } from "../types/stats";


export const sitesApi = {

    list: () => apiClient.get<SiteResponse[]>("/sites/"),

    get: (siteId: string) => apiClient.get<SiteResponse>(`/sites/${siteId}`),
    
    create: (data: SiteCreate) => apiClient.post<SiteResponse>("/sites/", data),

    delete: (siteId: string) => apiClient.delete(`/sites/${siteId}`),
    
    triggerHealthCheck: (siteId: string) => 
        apiClient.post<HealthCheckResponse>(`/sites/${siteId}/health-checks`),
    
    listHealthChecks: (siteId: string, limit: number = 100) => 
        apiClient.get<HealthCheckResponse[]>(`/sites/${siteId}/health-checks?limit=${limit}`),
    
    listDowntimes: (siteId: string, limit: number = 100) => 
        apiClient.get<DowntimeResponse[]>(`/sites/${siteId}/downtimes?limit=${limit}`),
    
    getDailyStats: (siteId: string, days: number = 7) =>
        apiClient.get<SiteDailyStatsResponse>(`/sites/${siteId}/stats?days=${days}`)

}