import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormsModule } from '@angular/forms';
import { Session } from '../session.service';
import { MatChipInputEvent, MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';

@Component({
    selector: 'app-session-edit-dialog',
    standalone: true,
    imports: [
        MatDialogModule,
        FormsModule,
        MatFormFieldModule,
        MatInputModule,
        MatButtonModule,
        MatChipsModule,
        MatIconModule
    ],
    templateUrl: './session-edit-dialog.component.html',
    styleUrl: './session-edit-dialog.component.css'
})
export class SessionEditDialogComponent {
    constructor(public dialogRef: MatDialogRef<SessionEditDialogComponent>, @Inject(MAT_DIALOG_DATA) public data: Session) { 
    }

    cancel(): void {
        this.dialogRef.close();
    }

    addChip(event: MatChipInputEvent): void {
        const value = (event.value || '').trim();
        if (value) {
            this.data.variables?.push(value);
        }
        event.chipInput!.clear();
    }

    removeChip(value: string): void {
        const variables = this.data?.variables as string[];
        const index = variables.indexOf(value);
        if (index >= 0) {
            variables.splice(index, 1);
        }
    }
}
