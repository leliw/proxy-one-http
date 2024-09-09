import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { ConfigService } from './config/config.service';
import { StatusViewComponent } from './proxy/status-view/status-view.component';

export interface Hello {
    Hello: string;
}
@Component({
    selector: 'app-root',
    standalone: true,
    imports: [CommonModule, RouterOutlet, StatusViewComponent],
    templateUrl: './app.component.html',
    styleUrl: './app.component.css'
})

export class AppComponent {

    title = 'frontend';
    hello = '';
    version = '';

    constructor(private http: HttpClient, private config: ConfigService) {
        this.http.get<Hello>('/api').subscribe(data => {
            this.hello = data.Hello;
        });
        this.config.getConfig().subscribe(c => {
            this.title = c.title;
            this.version = c.version;
        })
    }

}
