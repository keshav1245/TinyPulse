export interface DailyStat {

    date: string;
    total_checks: number;
    up_checks: number;
    down_checks: number;
    uptime_percentage: number | null;
    downtime_seconds: number;
    incident_count: number;

}

export interface SiteDailyStatsResponse {
    
    site_id: string;
    days: number;
    daily_stats: DailyStat[]

}