import { Routes } from '@angular/router';

export const routes: Routes = [
    {
        path: 'sessions', data: { title: "Zarejestrowane sesje HTTP" },
        loadComponent: () => import('./features/sessions/session-table/session-table.component').then(mod => mod.SessionTableComponent)
    },
    {
        path: 'sessions/create', data: { title: "Rejestrowanie sesji HTTP" },
        loadComponent: () => import('./features/sessions/session-start/session-start.component').then(mod => mod.SessionStartComponent)
    },
    {
        path: 'sessions/:sessionId/requests', data: { title: "Żądania sesji HTTP" },
        loadComponent: () => import('./features/sessions-requests/session-requests-table/session-requests-table.component').then(mod => mod.SessionRequestsTableComponent)
    },
    {
        path: 'sessions/:sessionId/requests/:reqId/view', data: { title: "Żądanie sesji HTTP" },
        loadComponent: () => import('./features/sessions-requests/session-request-view/session-request-view.component').then(mod => mod.SessionRequestViewComponent)
    },
    {
        path: 'sessions/:sessionId/replays/create',
        loadComponent: () => import('./features/sessions/session-replay/session-replay.component').then(mod => mod.SessionReplayComponent)
    },
    {
        path: 'sessions/:sessionId/replays',
        loadComponent: () => import('./features/sessions-replays/session-replay-table/session-replay-table.component').then(mod => mod.SessionReplayTableComponent)
    },
    {
        path: 'sessions/:sessionId/replays/:replayId/requests',
        loadComponent: () => import('./features/sessions-replays-requests/session-replay-request-table/session-replay-request-table.component').then(mod => mod.SessionReplayRequestTableComponent)
    },
    {
        path: 'sessions/:sessionId/replays/:replayId/requests/:reqId/view',
        loadComponent: () => import('./features/sessions-replays-requests/session-replay-request-view/session-replay-request-view.component').then(mod => mod.SessionReplayRequestViewComponent)
    },
];
