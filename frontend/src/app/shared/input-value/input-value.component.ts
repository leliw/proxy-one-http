import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef, MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormsModule } from '@angular/forms';
import { MatSelectModule } from '@angular/material/select';
import { Observable } from 'rxjs';


export interface InputValueData {
    title: string;
    prompt: string;
    label: string;
    options?: string[];
    options$?: Observable<string[]>
    value: any;
}

@Component({
    selector: 'input-value',
    templateUrl: './input-value.component.html',
    styleUrl: './input-value.component.css',
    standalone: true,
    imports: [
        MatDialogModule,
        FormsModule,
        MatFormFieldModule,
        MatInputModule,
        MatSelectModule,
        MatButtonModule
    ],
})
export class InputValueComponent {
    constructor(
        public dialogRef: MatDialogRef<InputValueComponent>,
        @Inject(MAT_DIALOG_DATA) public data: InputValueData,
    ) {
        if (data.options$)
            data.options$.subscribe(options => data.options = options);
    }

    cancel(): void {
        this.dialogRef.close();
    }
}