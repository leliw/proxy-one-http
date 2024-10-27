import { AfterViewInit, Component, inject, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTable, MatTableModule } from '@angular/material/table';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { MatSort, MatSortModule } from '@angular/material/sort';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { Session, SessionHeader, SessionService } from '../session.service';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { Router, RouterModule } from '@angular/router';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatTableDataSourceClientSide } from '../../../shared/mat-table-data-source-client-side';
import { FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatDialog } from '@angular/material/dialog';
import { MatMenuModule } from '@angular/material/menu';
import { SimpleDialogComponent } from '../../../shared/simple-dialog/simple-dialog.component';
import { InputValueComponent } from '../../../shared/input-value/input-value.component';
import { MatChipsModule } from '@angular/material/chips'
import { SessionEditDialogComponent } from '../session-edit-dialog/session-edit-dialog.component';

@Component({
    selector: 'app-session-table',
    standalone: true,
    imports: [
        CommonModule,
        RouterModule,
        FormsModule,
        MatTableModule,
        MatPaginatorModule,
        MatSortModule,
        MatProgressSpinnerModule,
        MatFormFieldModule,
        MatInputModule,
        MatButtonModule,
        MatIconModule,
        MatTooltipModule,
        MatMenuModule,
        MatChipsModule,
    ],
    templateUrl: './session-table.component.html',
    styleUrls: ['./session-table.component.css']
})
export class SessionTableComponent implements AfterViewInit {
    @ViewChild(MatPaginator) paginator!: MatPaginator;
    @ViewChild(MatSort) sort!: MatSort;
    @ViewChild(MatTable) table!: MatTable<Session>;

    displayedColumns: string[] = ['session_id', 'session_date', 'target_url', 'description', 'requests_cnt', 'variables', 'actions'];
    dataSource: MatTableDataSourceClientSide<Session>;

    constructor(private sessionService: SessionService, private router: Router) {
        this.dataSource = new MatTableDataSourceClientSide<Session>(this.sessionService.apiUrl);
    }

    ngAfterViewInit() {
        this.dataSource.sort = this.sort;
        this.dataSource.paginator = this.paginator;
        this.table.dataSource = this.dataSource;
    }

    viewRow(row: Session) {
        this.router.navigate(['/sessions', row.session_id, 'requests']);
    }

    replayRow(row: Session) {
        this.router.navigate(['/sessions', row.session_id, 'replays', 'create']);
    }

    viewReplaysRow(row: Session) {
        this.router.navigate(['/sessions', row.session_id, 'replays']);
    }

    private dialog = inject(MatDialog);

    editRow(row: Session) {
        let data = { ...row };
        data.variables = row.variables ? [... row.variables] : [];
        this.dialog.open(SessionEditDialogComponent, {
            data: data,
            width: '800px',
        }).afterClosed().subscribe((result) => {
            if (result) {
                row.description = result.description
                row.variables = result.variables
                this.sessionService.put(row.session_id, row).subscribe(() =>
                    this.dialog
                        .open(SimpleDialogComponent, {
                            data: {
                                title: 'Potwierdzenie',
                                message: `Sesja "<b>${row.session_id}</b>" została zmodyfikowana.`,
                                confirm: false
                            }
                        })
                )
            }
        });
    }


    deleteRow(row: Session) {
        this.dialog
            .open(SimpleDialogComponent, {
                data: {
                    title: 'Potwierdź kasowanie',
                    message: `Na pewno chesz skasować sesję "<b>${row.session_id}</b>"?` + (row.description ? `<hr/>${row.description}<hr/>` : ''),
                    confirm: true
                }
            })
            .afterClosed().subscribe(result => {
                if (result && row.session_id)
                    this.sessionService.delete(row.session_id).subscribe(res => {
                        this.dataSource.data = this.dataSource.data.filter(item => item.session_id !== row.session_id);
                        this.table.renderRows();
                        this.dialog
                            .open(SimpleDialogComponent, {
                                data: {
                                    title: 'Potwierdzenie',
                                    message: `Sesja "<b>${row.session_id}</b>" została skasowana.`,
                                    confirm: false
                                }
                            });
                    });
            });
    }
}