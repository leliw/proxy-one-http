import { Component, ViewChild, AfterViewInit, inject } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTableDataSourceClientSide } from '../../../shared/mat-table-data-source-client-side';
import { MatTable } from '@angular/material/table';
import { CommonModule } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatSortModule } from '@angular/material/sort';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { NavService } from '../../../shared/nav.service';
import { MatIconModule } from '@angular/material/icon';


export interface SessionReplayHeader {
    replay_id: string;
    replay_date: string;
    session_id: string;
    requests_cnt: number;
    description: string | null;
}

@Component({
    selector: 'app-replay-table',
    standalone: true,
    imports: [
        CommonModule,
        MatTableModule,
        MatPaginatorModule,
        MatSortModule,
        MatProgressSpinnerModule,
        MatFormFieldModule,
        MatInputModule,
        MatIconModule,
        FormsModule,
    ],
    templateUrl: './session-replay-table.component.html',
    styleUrls: ['./session-replay-table.component.css']
})
export class SessionReplayTableComponent implements AfterViewInit {
    displayedColumns: string[] = ['replay_id', 'replay_date', 'requests_cnt', 'description'];
    dataSource: MatTableDataSourceClientSide<SessionReplayHeader>;

    @ViewChild(MatPaginator) paginator!: MatPaginator;
    @ViewChild(MatSort) sort!: MatSort;
    @ViewChild(MatTable) table!: MatTable<SessionReplayHeader>;
    sessionId: string | null;


    constructor(route: ActivatedRoute, navService: NavService) {
        this.sessionId = route.snapshot.paramMap.get("sessionId");
        this.dataSource = new MatTableDataSourceClientSide<SessionReplayHeader>(
            `/api/sessions/${this.sessionId}/replays`
        );
        navService.setTitle(`Odtworzenia sesji: ${this.sessionId}`)
    }

    ngAfterViewInit(): void {
        this.dataSource.sort = this.sort;
        this.dataSource.paginator = this.paginator;
        this.table.dataSource = this.dataSource;
    }

    router = inject(Router);

    viewRow(row: SessionReplayHeader) {
        this.router.navigate(['sessions', row.session_id, 'replays', row.replay_id, 'requests']);
    }
}