import { HttpDownloadProgressEvent, HttpEventType } from '@angular/common/http';
import { Observable, Observer } from 'rxjs';
import { filter } from 'rxjs/operators';

export class StreamProcessor {

    /**
     * Przetwarzanie strumienia danych z odpowiedzi HTTP z użyciem typu generycznego
     * @param observableData Observable zwracający HttpEvent
     * @param chunkDelimiter Znak końca obiektu JSON, np. '\n'
     * @returns Observable emitujący obiekty dowolnego typu
     */
    public static processStream<T>(observableData: Observable<HttpDownloadProgressEvent>, chunkDelimiter: string = '\n'): Observable<T> {
        let lastCommaIndex = 0;
        let buffer = '';

        return new Observable((observer: Observer<T>) => {
            observableData.pipe(
                filter(event => event.type === HttpEventType.DownloadProgress && event.partialText !== undefined)
            ).subscribe({
                next: (event) => {
                    buffer = event.partialText ?? '';
                    let i;
                    while ((i = buffer.indexOf(chunkDelimiter, lastCommaIndex)) > -1) {
                        let jsonStr = buffer.substring(lastCommaIndex, i);
                        if (jsonStr.startsWith(',')) {
                            jsonStr = jsonStr.substring(1);  // Usuwanie ewentualnych nadmiarowych przecinków
                        }
                        lastCommaIndex = i + 1;
                        try {
                            const item = JSON.parse(jsonStr) as T;
                            observer.next(item);
                        } catch (e) {
                            console.error('Błąd parsowania JSON:', e);
                        }
                    }
                },
                error: (err) => observer.error(err),
                complete: () => {
                    buffer = buffer.substring(lastCommaIndex)
                    if (buffer) {
                        try {
                            const item = JSON.parse(buffer) as T;
                            observer.next(item);
                        } catch (e) {
                            console.error('Błąd parsowania JSON przy zamknięciu strumienia:', e);
                        }
                    }
                    observer.complete();
                }
            });
        });
    }
}
