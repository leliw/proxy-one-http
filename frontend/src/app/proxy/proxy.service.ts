import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export interface Status {
    status: string;
    port: number | undefined;
    target_url: string | undefined
}

@Injectable({
    providedIn: 'root'
})
export class ProxyService {

    private apiUrl = "/api/proxy"

    constructor(private http: HttpClient) { }

    getStatus(): Observable<Status> {
        return this.http.get<Status>(this.apiUrl + '/status');
    }

    start(): Observable<void> {
        return this.http.post<void>(this.apiUrl + '/start', '');
    }
    
    stop(): Observable<void> {
        return this.http.post<void>(this.apiUrl + '/stop', '');
    }

}
