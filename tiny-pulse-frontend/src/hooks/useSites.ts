import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import type { SiteCreate } from "../types/site";
import { sitesApi } from "../api/sites";



export function useSites() {
    return useQuery({
        queryKey: ["sites"],
        queryFn: sitesApi.list
    });
}

export function useSite(siteId: string){
    return useQuery({
        queryKey: ["sites", siteId],
        queryFn: () => sitesApi.get(siteId),
        enabled: !!siteId
    })
}

export function useCreateSite(){
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: (data: SiteCreate) => sitesApi.create(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["sites"] });
        }
    })
}

export function useTriggerHealthCheck(siteId: string){

    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: () => sitesApi.triggerHealthCheck(siteId),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["sites"] });
            queryClient.invalidateQueries({ queryKey: ["sites", siteId] });
            queryClient.invalidateQueries({ queryKey: ["sites", siteId, "health-checks"] })
        }
    })

}

export function useHealthChecks(siteId: string, limit: number = 100){
    return useQuery({
        queryKey: ["sites", siteId, "health-checks", limit],
        queryFn: () => sitesApi.listHealthChecks(siteId, limit),
        enabled: !!siteId,
    })
}

export function useDowntimes(siteId: string, limit: number = 100){
    return useQuery({
        queryKey: ["sites", siteId, "downtimes", limit],
        queryFn: () => sitesApi.listDowntimes(siteId, limit),
        enabled: !!siteId
    })
}

export function useDailyStas(siteId: string, days: number = 7){
    return useQuery({
        queryKey: ["sites", siteId, "stats", days],
        queryFn: () => sitesApi.getDailyStats(siteId, days),
        enabled: !!siteId,
    })
}