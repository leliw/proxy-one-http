import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { WebSocketSubject } from 'rxjs/webSocket';
import { WebSocketService } from '../../shared/web-socket.service';

export interface ProxyStatus {
    status: string;
    port: number;
    target_url: string
}

export interface ProxySettings {
    port: number;
    target_url: string;
    session_description?: string;
}


@Injectable({
    providedIn: 'root'
})
export class ProxyService {

    private apiUrl = "/api/proxy"
    private ws = new WebSocketService<string>(`${this.apiUrl}/logs`);

    constructor(private http: HttpClient) { }

    getStatus(): Observable<ProxyStatus> {
        return this.http.get<ProxyStatus>(this.apiUrl + '/status');
    }

    start(settings: ProxySettings): Observable<ProxyStatus> {
        return this.http.post<ProxyStatus>(this.apiUrl + '/start', settings);
    }

    stop(): Observable<ProxyStatus> {
        this.ws.close();
        return this.http.post<ProxyStatus>(this.apiUrl + '/stop', '');
    }

    logs(): WebSocketSubject<string> {
        return this.ws.connect()
    }
}
