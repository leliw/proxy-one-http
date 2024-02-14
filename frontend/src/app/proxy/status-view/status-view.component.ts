import { Component, OnInit } from '@angular/core';
import { ProxyService, Status } from '../proxy.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'proxy-status-view',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './status-view.component.html',
  styleUrl: './status-view.component.css'
})
export class StatusViewComponent implements OnInit {

    status!: Status;

    constructor(private proxyService: ProxyService) {}

    ngOnInit(): void {
        this.proxyService.getStatus().subscribe(status => this.status = status);
    }

    start(): void {
        this.status.status = "starting"
        this.proxyService.start().subscribe(status => this.status = status);
    }

    stop(): void {
        this.status.status = "stopping"
        this.proxyService.stop().subscribe(status => this.status = status);
    }

}
