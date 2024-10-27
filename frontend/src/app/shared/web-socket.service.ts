import { Injectable } from '@angular/core';
import { WebSocketSubject } from 'rxjs/internal/observable/dom/WebSocketSubject';


export class WebSocketService<T> {
    private devFrontendAddress = 'localhost:4200';
    private devBackendAddress = 'localhost:8000';
    private socketUrl!: string;
    private socket$: WebSocketSubject<T> | null = null;

    constructor(endpoint: string) {
        const url = new URL(window.origin);
        let host = url.host;
        // Replace the port of the host if the app is running in development mode
        host = host.replace(this.devFrontendAddress, this.devBackendAddress)
        this.socketUrl = `ws://${host}${endpoint}`;
    }

    public connect(): WebSocketSubject<T> {
        this.socket$ = new WebSocketSubject({
            url: this.socketUrl,
            deserializer: ({ data }) => data
        });
        return this.socket$;
    }

    public send(message: any): void {
        if (this.socket$)
            this.socket$.next(message);
        else
            throw Error("Not connected")
    }

    public close(): void {
        if (this.socket$)
            this.socket$.complete();
    }

}