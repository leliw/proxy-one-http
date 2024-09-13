import { Component, signal } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { SessionStartFromComponent } from "../session-start-from/session-start-from.component";

@Component({
    selector: 'app-session-start',
    standalone: true,
    imports: [
    MatCardModule,
    MatProgressBarModule,
    MatButtonModule,
],
    templateUrl: './session-start.component.html',
    styleUrl: './session-start.component.css'
})
export class SessionStartComponent {
    status = signal("READY");
    percent = signal(0);

    start(): void {
        this.status.set('IN PROGRESS');
    }

    stop(): void {
        this.status.set('CANCELED');
    }
}
