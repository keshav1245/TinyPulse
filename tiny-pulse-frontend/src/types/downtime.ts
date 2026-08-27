export interface DowntimeResponse {

    id: string;
    health_check_id: string;
    start_time: string;
    end_time: string | null;
    duration_seconds: number | null;

}