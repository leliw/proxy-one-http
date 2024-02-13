import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { ConfigService } from './config/config.service';

export interface Hello {
    Hello: string;
}
@Component({
    selector: 'app-root',
    standalone: true,
    imports: [CommonModule, RouterOutlet, HttpClientModule],
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
