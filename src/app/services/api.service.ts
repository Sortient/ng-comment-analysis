import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = '/api';
  constructor(private http: HttpClient) { }

  getAuthors(): Observable<any> {
    return this.http.get(`${this.baseUrl}/authors`);
  }

  getRankedAuthors(): Observable<any> {
    return this.http.get(`${this.baseUrl}/authors/ranked`);
  }

  getCommentStats(): Observable<any> {
    return this.http.get(`${this.baseUrl}/comments/stats`);
  }

  getTopComments(): Observable<any> {
    return this.http.get(`${this.baseUrl}/comments/top`);
  }

}
