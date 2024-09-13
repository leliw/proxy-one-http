import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export interface ProxyStatus {
    status: string;
    port: number;
    target_url: string
}

export interface ProxySettings {
    port: number;
    target_url: string
}

@Injectable({
    providedIn: 'root'
})
export class ProxyService {

    private apiUrl = "/api/proxy"

    constructor(private http: HttpClient) { }

    getStatus(): Observable<ProxyStatus> {
        return this.http.get<ProxyStatus>(this.apiUrl + '/status');
    }

    start(settings: ProxySettings): Observable<ProxyStatus> {
        return this.http.post<ProxyStatus>(this.apiUrl + '/start', settings);
    }

    stop(): Observable<ProxyStatus> {
        return this.http.post<ProxyStatus>(this.apiUrl + '/stop', '');
    }

}
