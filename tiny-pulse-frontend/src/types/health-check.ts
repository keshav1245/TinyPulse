import type { SiteStatus } from "./site";

export interface HealthCheckResponse {

    id: string;
    site_id: string;
    status_code: number | null;
    message: string | null;
    site_stat: SiteStatus;
    date_created: string;

}