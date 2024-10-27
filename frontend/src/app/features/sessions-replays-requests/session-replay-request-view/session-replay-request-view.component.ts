import { Component } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { SessionReplayRequest, SessionReplayRequestService } from '../session-replay-request.service';
import { CommonModule } from '@angular/common';
import { MatExpansionModule } from '@angular/material/expansion';
import { PropertiesComparisonTableComponent } from "../../../shared/properties-comparison-table/properties-comparison-table.component";

@Component({
    selector: 'app-session-replay-request-view',
    standalone: true,
    imports: [CommonModule, MatExpansionModule, PropertiesComparisonTableComponent],
    templateUrl: './session-replay-request-view.component.html',
    styleUrl: './session-replay-request-view.component.css'
})
export class SessionReplayRequestViewComponent {

    sessionId: string | null;
    replayId: string | null;
    reqId: string | null;
    data!: SessionReplayRequest;

    constructor(private sessionReplayRequestService: SessionReplayRequestService, private router: Router, activatedRoute: ActivatedRoute) {
        this.sessionId = activatedRoute.snapshot.paramMap.get("sessionId");
        this.replayId = activatedRoute.snapshot.paramMap.get("replayId");
        this.reqId = activatedRoute.snapshot.paramMap.get("reqId");
        if (this.sessionId && this.replayId && this.reqId)
            this.sessionReplayRequestService.get(this.sessionId, this.replayId, this.reqId).subscribe(data => this.data = data);
    }
}
