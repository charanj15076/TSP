import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

 
export interface Result {
  data: any;
  status: string;
}

@Injectable({
  providedIn: 'root'
})
export class RoutesService {
  constructor(private http: HttpClient) {}
 
  runTSP(postData: any): Observable<Result> {
    return this.http.post<Result>(
      `${environment.baseUrl}/run`,
      { 
        destination_list: postData.destinationList,
        technique: postData.technique,
      }
    );
  }
}
