import { Injectable } from '@angular/core';
import { HttpClient, HttpDownloadProgressEvent, HttpEventType } from '@angular/common/http';
import { filter, Observable } from 'rxjs';
import { StreamProcessor } from '../../shared/stream-processor';

export interface SessionHeader {
    session_id: string;
    session_date: string;
    target_url: string;
    requests_cnt: number;
    variables: string[] | undefined;
    description: string | undefined;
}

export interface Session extends SessionHeader {
}
    

export interface ReplayRequest {
    req_id: string;
    url: string;
    method: string;
    status_code: number;
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

    replay(sessionId: string): Observable<ReplayRequest> {
        const httpObservable = this.http.post(`${this.apiUrl}/${sessionId}/replays`, {}, {
            responseType: 'text',
            reportProgress: true,
            observe: 'events'
        }) as Observable<HttpDownloadProgressEvent>;

        // Użycie nowego StreamProcessor do obsługi strumieniowego przetwarzania ReplayRequest
        return StreamProcessor.processStream<ReplayRequest>(httpObservable);
    }

}