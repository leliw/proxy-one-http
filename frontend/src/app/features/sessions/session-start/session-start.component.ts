import { Component, signal, ViewChild } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { SessionStartFormComponent } from "../session-start-form/session-start-form.component";

@Component({
    selector: 'app-session-start',
    standalone: true,
    imports: [
        MatCardModule,
        MatProgressBarModule,
        MatButtonModule,
        SessionStartFormComponent
    ],
    templateUrl: './session-start.component.html',
    styleUrl: './session-start.component.css'
})
export class SessionStartComponent {
    @ViewChild(SessionStartFormComponent) paramsForm!: SessionStartFormComponent;
    status = signal("READY");
    percent = signal(0);

    start(): void {
        const params = this.paramsForm.onSubmit();
        if (params) {
            this.status.set('IN PROGRESS');
        }
    }

    stop(): void {
        this.status.set('CANCELED');
    }
}
