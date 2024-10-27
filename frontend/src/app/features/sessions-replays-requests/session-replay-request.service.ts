import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { SessionRequest } from '../sessions-requests/session-request.service';

export interface SessionReplayRequestHeader {
    req_id: string;
    start: Date;
    end: Date | null;
    url: string;
    method: string;
    status_code: number | null;
    resp_content_length: number | null;
    resp_content_type: string | null;
    cached: boolean | null;
    disabled: boolean | null;
    duration: string | null;
}

export interface SessionReplayRequest {
    req_id: string;
    url: string;
    method: string;
    org: SessionRequest;
    repl: SessionRequest;
    diff: string;
    diff_dict: {};
  }



@Injectable({
    providedIn: 'root'
})
export class SessionReplayRequestService {

    constructor(private http: HttpClient) { }

    private apiUrl(session_id: string, replay_id: string): string {
        return `/api/sessions/${session_id}/replays/${replay_id}/requests`;
    }


    getAll(session_id: string, replay_id: string): Observable<SessionReplayRequestHeader[]> {
        return this.http.get<SessionReplayRequestHeader[]>(this.apiUrl(session_id, replay_id));
    }

    get(session_id: string, replay_id: string, req_id: string): Observable<SessionReplayRequest> {
        return this.http.get<SessionReplayRequest>(`${this.apiUrl(session_id, replay_id)}/${req_id}`);
    }

    create(session_id: string, replay_id: string, sessionReplayRequest: SessionReplayRequest): Observable<SessionReplayRequest> {
        return this.http.post<SessionReplayRequest>(this.apiUrl(session_id, replay_id), sessionReplayRequest);
    }

    update(session_id: string, replay_id: string, req_id: string, sessionReplayRequest: SessionReplayRequest): Observable<SessionReplayRequest> {
        return this.http.put<SessionReplayRequest>(`${this.apiUrl(session_id, replay_id)}/${req_id}`, sessionReplayRequest);
    }

    delete(session_id: string, replay_id: string, req_id: string): Observable<void> {
        return this.http.delete<void>(`${this.apiUrl(session_id, replay_id)}/${req_id}`);
    }
}