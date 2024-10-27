import { Component, ViewChild, AfterViewInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTable, MatTableModule } from '@angular/material/table';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { MatSort, MatSortModule } from '@angular/material/sort';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatTableDataSourceClientSide } from '../../../shared/mat-table-data-source-client-side';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { NavService } from '../../../shared/nav.service';
import { animate, state, style, transition, trigger } from '@angular/animations';
import { MatButtonModule } from '@angular/material/button';

interface SessionReplayRequest {
    req_id: string;
    start: Date;
    end: Date;
    url: string;
    method: string;
    org_status_code: number;
    status_code: number;
    resp_content_length: number;
    resp_content_type: string;
    request_headers: {};
    request_body_form: {};
    request_body_str: string;
    request_body_bytes: string;
    response_headers: {};
    response_body_json: {};
    response_body_form_values: {};
    response_body_str: string;
    response_body_bytes: string;
    diff: string;
    duration: string;
    diff_dict: Record<string, String> | null;
}

@Component({
    selector: 'app-session-replay-request-table',
    standalone: true,
    imports: [
        CommonModule,
        MatTableModule,
        MatPaginatorModule,
        MatSortModule,
        FormsModule,
        MatFormFieldModule,
        MatInputModule,
        MatButtonModule,
        MatIconModule,
        MatProgressSpinnerModule,
    ],
    animations: [
        trigger('detailExpand', [
            state('collapsed,void', style({ height: '0px', minHeight: '0' })),
            state('expanded', style({ height: '*' })),
            transition('expanded <=> collapsed', animate('225ms cubic-bezier(0.4, 0.0, 0.2, 1)')),
        ]),
    ],
    templateUrl: './session-replay-request-table.component.html',
    styleUrl: './session-replay-request-table.component.css'
})
export class SessionReplayRequestTableComponent implements AfterViewInit {
    @ViewChild(MatPaginator) paginator!: MatPaginator;
    @ViewChild(MatSort) sort!: MatSort;
    @ViewChild(MatTable) table!: MatTable<SessionReplayRequest>;

    dataSource: MatTableDataSourceClientSide<SessionReplayRequest>;

    displayedColumns: string[] = ['req_id', 'start', 'end', 'url', 'method', 'status_code', 'duration', 'resp_content_type', 'resp_content_length', 'expand'];

    sessionId: string | null;
    replayId: string | null;

    expandedElement: SessionReplayRequest | null = null;


    constructor(route: ActivatedRoute, navService: NavService) {
        this.sessionId = route.snapshot.paramMap.get("sessionId");
        this.replayId = route.snapshot.paramMap.get("replayId");
        this.dataSource = new MatTableDataSourceClientSide<SessionReplayRequest>(
            `/api/sessions/${this.sessionId}/replays/${this.replayId}/requests`
        );
        navService.setTitle(`Sesja: ${this.sessionId}, odtworzenie ${this.replayId}`)
    }

    ngAfterViewInit() {
        this.dataSource.sort = this.sort;
        this.dataSource.paginator = this.paginator;
        this.table.dataSource = this.dataSource;
    }

    expandRow(row: SessionReplayRequest) {
        if (row.diff)
            this.expandedElement = this.expandedElement === row ? null : row
    }

    router = inject(Router);

    viewRow(row: SessionReplayRequest) {
        this.router.navigate(['sessions', this.sessionId, 'replays', this.replayId, 'requests', row.req_id, 'view']);
    }
}