import { API_BASE_URL } from "../constants";

export class ApiError extends Error {

    status: number;

    constructor(message: string, status: number){

        super(message);
        this.name = "ApiError";
        this.status = status;

    }

}


async function request<T>(path: string, 
        options: RequestInit = {}): Promise<T> {
    
    
    const res = await fetch(`${API_BASE_URL}${path}`,{
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...options.headers,
        },
    });


    if(!res.ok){
        let message = res.statusText;
        try {
            const body = await res.json();
            message = body.detail ?? message;
        }catch {
            //No JSON Body here so ignore.
        }

        throw new ApiError(message, res.status);

    }

    if(res.status === 204){
        return undefined as T;
    }

    return res.json() as Promise<T>;

}

export const apiClient = {
    get: <T>(path: string) => request<T>(path),
    post: <T>(path: string, body?: unknown) => 
        request<T>(path, {
            method: "POST",
            body: body ? JSON.stringify(body) : undefined
        }),
}
