import { Component, inject } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { ActivatedRoute, Router } from '@angular/router';
import { SessionRequest, SessionRequestService } from '../session-request.service';
import { CommonModule } from '@angular/common';
import { MatExpansionModule } from '@angular/material/expansion';
import { NavService } from '../../../shared/nav.service';

@Component({
    selector: 'app-session-request-view',
    standalone: true,
    imports: [
        CommonModule,
        MatCardModule,
        MatExpansionModule,
    ],
    templateUrl: './session-request-view.component.html',
    styleUrl: './session-request-view.component.css'
})
export class SessionRequestViewComponent {
    sessionId!: string;
    reqId!: string;
    data!: SessionRequest;

    constructor(
        private sessionRequestService: SessionRequestService,
        private router: Router,
        route: ActivatedRoute,
        navService: NavService,
    ) {
        route.params.subscribe(params => {
            this.sessionId = params['sessionId'];
            this.reqId = params['reqId'];
            navService.setTitle(`Sesja: ${this.sessionId}, żądanie HTTP: ${this.reqId}`)
            this.sessionRequestService.get(this.sessionId, this.reqId).subscribe({
                next: (request) => this.data = request,
                error: (error) => this.onError('Error fetching session request data:', error)
            });
        });
    }

    onError(message: string, error: Error): void {
        console.error(message, error);
        // Handle error
    }
}