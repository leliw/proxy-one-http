import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, map, of } from 'rxjs';

export interface Config {
    title: string;
    version: string;
}

@Injectable({
  providedIn: 'root',
})
export class ConfigService {

    private url = "/api/config"
    private static config: Config | undefined = undefined;

    constructor(private http: HttpClient) { }
    
    public getConfig(): Observable<Config> {
        if (!ConfigService.config)
            return this.http.get<Config>(this.url)
                .pipe(map(c => {
                    if (!c.version)
                        c.version = "0.0.1";
                    ConfigService.config = c;
                    return c;
                }));
        else
            return of(ConfigService.config);
    }

}
