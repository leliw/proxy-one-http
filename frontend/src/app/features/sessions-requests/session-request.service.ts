import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export interface ProxyRequestHeader {
    req_id: string;
    start: string;
    end: string;
    url: string;
    method: string;
    status_code: number;
    resp_content_length: number;
    resp_content_type: string;
    duration: string;
    cached: boolean;
    disabled: boolean;
    description: string;
}

export interface SessionRequest extends ProxyRequestHeader{
    request_headers: { [key: string]: string };
    request_body_form: { [key: string]: string };
    request_body_str: string;
    request_body_bytes: string;
    response_headers: { [key: string]: string };
    response_body_json: { [key: string]: any }; // Use any since the structure can be variable
    response_body_form_values: { [key: string]: any }
    response_body_str: string;
    response_body_bytes: string;
}

export interface SessionRequestPatch {
    disabled?: boolean;
    description?: string;
}

@Injectable({
    providedIn: 'root'
})
export class SessionRequestService {
    private apiUrl = '/api/sessions';

    constructor(private http: HttpClient) { }

    get(session_id: string, req_id: string): Observable<SessionRequest> {
        return this.http.get<SessionRequest>(`${this.apiUrl}/${session_id}/requests/${req_id}`);
    }

    patch(session_id: string, req_id: string, data: SessionRequestPatch): Observable<void> {
        return this.http.patch<void>(`${this.apiUrl}/${session_id}/requests/${req_id}`, data);
    }
}
