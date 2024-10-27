import { Injectable, signal } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { ActivationStart, NavigationEnd, Router } from '@angular/router';
import { Title } from '@angular/platform-browser';

@Injectable({
    providedIn: 'root'
})
export class NavService {
    private appTitle!: string;
    private nextPageTitle?: string;
    title = signal("")
    breadcrumb: string[] = [];

    constructor(private router: Router, private browserTitle: Title) {
        // Pobieram tytuł strony, jako domyślny tytuł stron
        // które nie mają zdefiniowanego tytułu
        this.appTitle = browserTitle.getTitle();
        this.title.set(this.appTitle);
        this.router.events
            .subscribe(event => {
                if (event instanceof ActivationStart) {
                    // Pobieram tytuł strony z danych routingu, a
                    // jeśli nie ma, to biorę domyślny i zapisuję na boku
                    this.nextPageTitle = (event as ActivationStart).snapshot.data["title"] ?? this.appTitle;
                    const path = (event as ActivationStart).snapshot.routeConfig?.path;
                    if (path) {
                        const url = "/" + decodeURIComponent((event as ActivationStart).snapshot.url.join("/"));
                        if (path.includes(":")) {
                            // Routing path contain parameter - add
                            // current url to breadcrumb
                            const index = this.breadcrumb.indexOf(url);
                            if (index == -1)
                                this.breadcrumb.push(url)
                            else
                                this.breadcrumb.splice(index + 1)
                        } else
                            this.breadcrumb = [url]
                    }
                } else if (event instanceof NavigationEnd && this.nextPageTitle) {
                    // Jeśli komponent nie ustawił tytuły w konstruktorze lub w onInit()
                    // to stawiam ten co zapisałem na boku
                    this.setTitle(this.nextPageTitle)
                }
            });
    }
    /**
     * Ustawia tytuł aktualnej strony
     * @param title 
     */
    public setTitle(title: string) {
        this.nextPageTitle = undefined;
        this.title.set(title);
    }

    backRoute(): string | undefined {
        if (this.breadcrumb.length > 1)
            return this.breadcrumb[this.breadcrumb.length - 2];
        else
            return undefined;
    }
}
