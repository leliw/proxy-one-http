import { Component, inject, signal, ViewChild } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { SessionStartFormComponent } from "../session-start-form/session-start-form.component";
import { ProxyService } from '../../proxy/proxy.service';

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
    service = inject(ProxyService);
    status = signal("READY");
    percent = signal(0);

    start(): void {
        const proxySettings = this.paramsForm.onSubmit();
        if (proxySettings)
            this.service.start(proxySettings).subscribe(() => {
                this.status.set('IN PROGRESS');
                window.open(`http://localhost:${proxySettings.port}`, "proxy")
            });
    }

    stop(): void {
        this.service.stop().subscribe(() => this.status.set('CANCELED'));
    }
}
