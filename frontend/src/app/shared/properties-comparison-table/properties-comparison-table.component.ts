import { CommonModule } from '@angular/common';
import { Component, Input, OnInit, ViewEncapsulation } from '@angular/core';

@Component({
    selector: 'app-properties-comparison-table',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './properties-comparison-table.component.html',
    styleUrl: './properties-comparison-table.component.css',
    encapsulation: ViewEncapsulation.None
})
export class PropertiesComparisonTableComponent implements OnInit {
    @Input() keys: string[] | Set<string> | undefined;
    @Input({ required: true }) first!: { [key: string]: string } | any;
    @Input({ required: true }) second!: { [key: string]: string } | any;
    
    @Input() propertyHeader: string = "Properties"
    @Input() firstHeader: string = "First"
    @Input() secondHeader: string = "Second"


    ngOnInit(): void {
        if (!this.keys)
            this.keys = new Set([...Object.keys(this.first), ...Object.keys(this.second)])
    }
}
