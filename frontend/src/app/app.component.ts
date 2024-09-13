import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { ConfigService } from './core/config.service';
import { StatusViewComponent } from './proxy/status-view/status-view.component';
import { NavComponent } from "./core/nav/nav.component";

export interface Hello {
    Hello: string;
}
@Component({
    selector: 'app-root',
    standalone: true,
    imports: [CommonModule, RouterOutlet, StatusViewComponent, NavComponent],
    templateUrl: './app.component.html',
    styleUrl: './app.component.css'
})

export class AppComponent {

    version = '';

    constructor(private config: ConfigService) {
        this.config.getConfig().subscribe(c => {
            this.version = c.version;
        })
    }

}
