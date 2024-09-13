import { HttpClient, HttpResponse } from "@angular/common/http";
import { EventEmitter, inject } from "@angular/core";
import { MatTableDataSource } from "@angular/material/table";
import { ActivatedRoute, Params, Router } from "@angular/router";
import { BehaviorSubject, filter, merge, Observable, tap } from "rxjs";


/**
 * Źródło danych dla tabeli w fitlrowaniem, paginacją
 * i sortowaniem po stronie klienta.
 * 
 * @author Marcin Leliwa
 */
export class MatTableDataSourceClientSide<ItemType> extends MatTableDataSource<ItemType> {
    protected http = inject(HttpClient);
    protected router = inject(Router);
    protected activatedRoute =inject(ActivatedRoute);
    /**
     * Znacznik, że dane są ładowane z serwera
     */
    isLoading = false;
    /**
     * Parametry query, które są parsowane, jeśli nie podano,
     * to jest przetwarzany activatedRoute
    */
    queryParams?: Params;
    /**
     * Filtr do wyszukiwania pełnotekstowego, 
     * dodatkowo emituje zdarzenie do aktualizacji url
     */
    override set filter(s: string) {
        super.filter = s;
        this.filterChange.emit();
    }
    override get filter(): string {
        return super.filter;
    }
    private filterChange = new EventEmitter<void>();
    
    /**
     * Podanie wszystkich parametrów tworzy "full automat".
     * Nic nie podając, trzeba obsłużyć "ręcznie".
     * 
     * @param apiUrl - mozna podać URL do domyślnego pobierania danych z serwera http
     */
    constructor(private apiUrl?: string) {
        super();
    }

    /**
     * Pobiera dane z serwera, 
     * na czas pobierania ustawia isLoading,
     * parsuje parametry query oraz 
     * ustawia aktualizację parametrów query po zmianie filtra, strony lub sortowania
     * 
     * @returns 
     */
    override connect(): BehaviorSubject<ItemType[]> {
        const t = setTimeout(() => this.isLoading = true, 10);
        this.getData()
            .pipe(
                filter(response => response.ok),
                tap(() => { clearTimeout(t); this.isLoading = false; })
            )
            .subscribe((response) => {
                this.data = response.body || [];
                if (this.queryParams)
                    this.parseParams(this.queryParams);
                else if (this.activatedRoute)
                    this.activatedRoute.queryParams.subscribe((params) => { this.parseParams(params); });
            });
        if (this.paginator && this.sort)
            merge(this.filterChange, this.paginator.page, this.sort.sortChange).subscribe(() => { this.updateUrl(this.createParams()); });
        return super.connect();
    }

    /**
     * Pobranie danych z serwera HTTP (można przykryć i wywołać przez serwis)
     * 
     * @param params parametry query
     * @returns 
     */
    public getData(): Observable<HttpResponse<ItemType[]>> {
        if (this.http && this.apiUrl)
            return this.http.get<ItemType[]>(this.apiUrl, { observe: 'response' });
        else
            throw new Error('Dla domyślnego pobierania danych treba podać http i apiUrl.');
    }

    /**
     * Metoda pomocnicza - nie musi być używana
     */
    public applyFilter(event: Event) {
        const filterValue = (event.target as HTMLInputElement).value;
        this.filter = filterValue.trim().toLowerCase();
    }

    /**
     * Tworzy parametry query
     */
    private createParams(): Params {
        let params: Params = {};
        if (this.filter)
            params["q"] = this.filter;
        if (this.sort && this.sort.active && this.sort.direction !== '') {
            params["order"] = (this.sort.direction === "asc" ? "" : "-") + this.sort.active;
        }
        if (this.paginator && this.paginator.pageIndex != 0) {
            params["page"] = (this.paginator.pageIndex + 1).toString();
            params["perPage"] = this.paginator.pageSize.toString();
        }
        return params;
    }

    /**
     * Aktualizuje aktualny URL wg parametrów filtrujących itp.
     * Można przykryć.
     * 
     * @param params 
     */
    updateUrl(params: Params) {
        if (this.router)
            this.router.navigate([],
                {
                    relativeTo: this.activatedRoute,
                    queryParams: params
                });
    }

    /**
     * Przetwarza listę (mapę) parametrów 
     * odpowiednio ustawiając obietkty filtrujące,
     * paginacji i sortowania
     * @param params 
     */
    public parseParams(params: Params) {
        if (params["q"]) {
            this.filter = params["q"];
        }
        this.parseSortParam(params);
        this.parsePaginatorParams(params);
    }

    /**
     * Parsowania parametru sortowania
     * @param params 
     */
    private parseSortParam(params: Params) {
        if (this.sort && params["order"]) {
            let val = params["order"];
            if (val.startsWith("-")) {
                this.sort.direction = "desc";
                this.sort.active = val.substring(1);
            } else {
                this.sort.direction = "asc"
                this.sort.active = val;
            }
            this.sort.sortChange.emit();
        }
    }

    /**
     * Parsowanie parametrów paginacji
     * @param params 
     */
    private parsePaginatorParams(params: Params) {
        if (this.paginator) {
            this.paginator.pageIndex = (+params["page"] - 1) || 0;
            if (params["perPage"])
                this.paginator.pageSize = +params["perPage"];
            this.paginator.page.emit();
        }
    }

}