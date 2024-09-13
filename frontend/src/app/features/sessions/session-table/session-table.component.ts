import { Component, inject, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTable, MatTableModule } from '@angular/material/table';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { MatSort, MatSortModule } from '@angular/material/sort';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { Session, SessionHeader, SessionService } from '../session.service';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { Router } from '@angular/router';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatTableDataSourceClientSide } from '../../../shared/mat-table-data-source-client-side';
import { FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';

@Component({
    selector: 'app-session-table',
    standalone: true,
    imports: [
        CommonModule,
        FormsModule,
        MatTableModule,
        MatPaginatorModule,
        MatSortModule,
        MatProgressSpinnerModule,
        MatFormFieldModule,
        MatInputModule,
        MatButtonModule,
        MatIconModule,
    ],
    templateUrl: './session-table.component.html',
    styleUrls: ['./session-table.component.css']
})
export class SessionTableComponent {
    @ViewChild(MatPaginator) paginator!: MatPaginator;
    @ViewChild(MatSort) sort!: MatSort;
    @ViewChild(MatTable) table!: MatTable<Session>;

    displayedColumns: string[] = ['session_id', 'session_date', 'target_url', 'description', 'requests_cnt', 'actions'];
    dataSource: MatTableDataSourceClientSide<Session>;

    constructor(private sessionService: SessionService, private router: Router) {
        this.dataSource = new MatTableDataSourceClientSide<Session>(this.sessionService.apiUrl);
    }

    ngAfterViewInit() {
        this.dataSource.sort = this.sort;
        this.dataSource.paginator = this.paginator;
        this.table.dataSource = this.dataSource;
    }

    viewSession(sessionId: string) {
        this.router.navigate(['/sessions', sessionId]);
    }

    deleteSession(sessionId: string) {
        // Implement logic for deleting a session
    }
}