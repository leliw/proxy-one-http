import { Routes } from '@angular/router';

export const routes: Routes = [
    {
        path: 'sessions', data: { title: "Zarejestrowane sesje HTTP"},
        loadComponent: () => import('./features/sessions/session-table/session-table.component').then(mod => mod.SessionTableComponent)
    },
];
