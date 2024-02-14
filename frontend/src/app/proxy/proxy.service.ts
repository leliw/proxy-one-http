import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export interface Status {
    status: string;
    port: number;
    target_url: string
}

export interface Settings {
    port: number;
    target_url: string
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

    start(settings: Settings): Observable<Status> {
        return this.http.post<Status>(this.apiUrl + '/start', settings);
    }

    stop(): Observable<Status> {
        return this.http.post<Status>(this.apiUrl + '/stop', '');
    }

}
