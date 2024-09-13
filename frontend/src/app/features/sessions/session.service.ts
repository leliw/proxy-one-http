import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface SessionHeader {
    session_id: string;
    session_date: string;
    target_url: string;
    requests_cnt: number;
    description: string | undefined;
}

export interface Session extends SessionHeader {

}

@Injectable({
    providedIn: 'root'
})
export class SessionService {
    apiUrl = '/api/sessions';

    constructor(private http: HttpClient) { }

    get(sessionId: string): Observable<Session> {
        return this.http.get<Session>(`${this.apiUrl}/${sessionId}`);
    }

    getAll(): Observable<SessionHeader[]> {
        return this.http.get<SessionHeader[]>(this.apiUrl);
    }

    post(session: Session): Observable<Session> {
        return this.http.post<Session>(this.apiUrl, session);
    }

    put(sessionId: string, session: Session): Observable<Session> {
        return this.http.put<Session>(`${this.apiUrl}/${sessionId}`, session);
    }

    delete(sessionId: string): Observable<boolean> {
        return this.http.delete<boolean>(`${this.apiUrl}/${sessionId}`);
    }
}