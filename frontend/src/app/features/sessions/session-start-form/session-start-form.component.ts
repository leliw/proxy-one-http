import { Component, inject } from '@angular/core';
import { FormBuilder, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { ProxySettings } from '../../proxy/proxy.service';


@Component({
    selector: 'app-session-start-form',
    standalone: true,
    imports: [
        FormsModule,
        ReactiveFormsModule,
        MatFormFieldModule,
        MatInputModule,
    ],
    templateUrl: './session-start-form.component.html',
    styleUrl: './session-start-form.component.css'
})
export class SessionStartFormComponent {
    fb = inject(FormBuilder);
    form = this.fb.nonNullable.group({
        target_url: ['https://', [Validators.required, Validators.minLength(10)]],
        port: [8999, [Validators.required, Validators.min(8000), Validators.max(8999)]],
        session_description: '',
    })

    onSubmit(): ProxySettings | undefined {
        if (this.form.invalid) return undefined;
        else return this.form.getRawValue() as ProxySettings;
    }
}