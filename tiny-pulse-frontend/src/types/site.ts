import type { HealthCheckResponse } from "./health-check"

export type SiteStatus = "UP" | "DOWN"

export interface SiteBase {

    url: string;
    name: string;
    interval: number;

}

export interface SiteCreate extends SiteBase {
    
    is_active: boolean;

}

export interface SiteResponse extends SiteCreate {

    site_id: string;
    latest_health_check: HealthCheckResponse | null;

}