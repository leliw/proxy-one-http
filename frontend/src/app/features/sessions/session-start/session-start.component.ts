import { Component, ElementRef, inject, signal, ViewChild } from '@angular/core';
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
    @ViewChild('container') container!: ElementRef;
    service = inject(ProxyService);
    status = signal("READY");
    percent = signal(0);
    data: string[] = []; 

    start(): void {
        const proxySettings = this.paramsForm.onSubmit();
        if (proxySettings) {
            const urlObject = new URL(proxySettings.target_url);
            const address = urlObject.origin;
            const path = urlObject.pathname;
            proxySettings.target_url = address
            this.service.start(proxySettings).subscribe(() => {
                this.status.set('IN PROGRESS');
                window.open(`http://localhost:${proxySettings.port}/${path}`, "proxy", "incognito=yes");
                this.service.logs().subscribe(data => {
                    this.data.push(data);
                    this.container.nativeElement.scrollTop = this.container.nativeElement.scrollHeight;
                });
            });
        }
    }

    stop(): void {
        this.service.stop().subscribe(() => this.status.set('CANCELED'));
    }
}
