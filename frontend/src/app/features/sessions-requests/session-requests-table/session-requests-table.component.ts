import { Component, inject, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatSortModule } from '@angular/material/sort';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatTableDataSourceClientSide } from '../../../shared/mat-table-data-source-client-side';
import { ActivatedRoute, Router } from '@angular/router';
import { MatTable } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { FormsModule } from '@angular/forms';
import { NavService } from '../../../shared/nav.service';
import { MatTooltipModule } from '@angular/material/tooltip';
import { ProxyRequestHeader, SessionRequestService } from '../session-request.service';
import { MatDialog } from '@angular/material/dialog';
import { InputValueComponent } from '../../../shared/input-value/input-value.component';


@Component({
    selector: 'app-session-requests-table',
    standalone: true,
    imports: [
        CommonModule,
        FormsModule,
        MatTableModule,
        MatPaginatorModule,
        MatSortModule,
        MatFormFieldModule,
        MatInputModule,
        MatIconModule,
        MatTooltipModule,
        MatProgressSpinnerModule,
    ],
    templateUrl: './session-requests-table.component.html',
    styleUrl: './session-requests-table.component.css',
})
export class SessionRequestsTableComponent {
    @ViewChild(MatPaginator) paginator!: MatPaginator;
    @ViewChild(MatSort) sort!: MatSort;
    @ViewChild(MatTable) table!: MatTable<ProxyRequestHeader>;
    dataSource!: MatTableDataSourceClientSide<ProxyRequestHeader>;

    displayedColumns: string[] = [
        'req_id',
        'start',
        'end',
        'duration',
        'url',
        'method',
        'status_code',
        'resp_content_type',
        'resp_content_length',
        'description',
        'cached',
        'disabled'
    ];
    sessionId!: string | null;

    constructor(route: ActivatedRoute, navService: NavService) {
        this.sessionId = route.snapshot.paramMap.get("sessionId");
        this.dataSource = new MatTableDataSourceClientSide<ProxyRequestHeader>(
            `/api/sessions/${this.sessionId}/requests`
        );
        navService.setTitle(`Żądania HTTP w sesji: ${this.sessionId}`)
    }

    ngAfterViewInit(): void {
        this.dataSource.sort = this.sort;
        this.dataSource.paginator = this.paginator;
        this.table.dataSource = this.dataSource;
    }

    router = inject(Router);

    viewRow(row: ProxyRequestHeader) {
        this.router.navigate(['sessions', this.sessionId, 'requests', row.req_id, 'view']);
    }

    service = inject(SessionRequestService)

    switchDisabled(row: ProxyRequestHeader) {
        if (this.sessionId) {
            this.service.patch(this.sessionId, row.req_id, { disabled: !row.disabled })
                .subscribe(() => row.disabled = !row.disabled)
        }
    }

    dialog = inject(MatDialog);

    editDescription(row: ProxyRequestHeader) {
        this.dialog.open(InputValueComponent, {
            data: {
                title: 'Edit description',
                prompt: 'Request id: ' + row.req_id,
                label: 'Description',
                value: row.description
            },
            width: '800px',
        }).afterClosed().subscribe((result) => {
            if (result && this.sessionId) {
                console.log('Input value:', result);
                this.service.patch(this.sessionId, row.req_id, { description: result })
                    .subscribe(() => row.description = result)
            }
        });
    }

}