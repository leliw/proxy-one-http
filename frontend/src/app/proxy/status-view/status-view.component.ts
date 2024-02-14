import { Component, OnInit } from '@angular/core';
import { ProxyService, Settings, Status } from '../proxy.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'proxy-status-view',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './status-view.component.html',
  styleUrl: './status-view.component.css'
})
export class StatusViewComponent implements OnInit {

    status!: Status;
    settings!: Settings;

    constructor(private proxyService: ProxyService) {}

    ngOnInit(): void {
        this.proxyService.getStatus().subscribe(status => {
            this.status = status
            this.settings = {port: status.port, target_url: status.target_url}
        });
    }

    start(): void {
        this.status.status = "starting"
        this.proxyService.start(this.settings).subscribe(status => this.status = status);
    }

    stop(): void {
        this.status.status = "stopping"
        this.proxyService.stop().subscribe(status => this.status = status);
    }

}
