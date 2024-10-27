import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, map, of } from 'rxjs';

export interface Config {
    version: string;
}

export interface UserConfig {
    target_url: string
    port: number
}

@Injectable({
    providedIn: 'root',
})
export class ConfigService {

    private url = "/api/config"
    private static config: Config | undefined = undefined;
    private static userConfig: UserConfig | undefined = undefined;

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

    public getUserConfig(): Observable<UserConfig> {
        if (!ConfigService.userConfig)
            return this.http.get<UserConfig>(`${this.url}/user`)
                .pipe(map(c => {
                    ConfigService.userConfig = c;
                    return c;
                }));
        else
            return of(ConfigService.userConfig);
    }

    public setUserConfig(userConfig: UserConfig): void {
        ConfigService.userConfig = userConfig
        this.http.put<void>(`${this.url}/user`, userConfig).subscribe();
    }

}
