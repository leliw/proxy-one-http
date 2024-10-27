import { Component, inject } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { ReplayRequest, SessionService } from '../session.service';
import { ActivatedRoute, ActivatedRouteSnapshot } from '@angular/router';
import { NavService } from '../../../shared/nav.service';

@Component({
    selector: 'app-session-replay',
    standalone: true,
    imports: [
        MatCardModule,
    ],
    templateUrl: './session-replay.component.html',
    styleUrl: './session-replay.component.css'
})
export class SessionReplayComponent {
    data: ReplayRequest[] = []

    sessionService = inject(SessionService)
    navService = inject(NavService)

    constructor(activeRoute: ActivatedRoute) {
        const sessionId = activeRoute.snapshot.paramMap.get("sessionId");
        this.navService.setTitle(`Odtwarzanie sesji HTTP: ${sessionId}`)
        if (sessionId) {
            this.sessionService.replay(sessionId).subscribe(o => this.data.push(o));
        }
    }
}
