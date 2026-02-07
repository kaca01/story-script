import { Observable } from "rxjs";
import { StoryOption, StoryState } from "../../models";
import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class StoryService {
  private baseUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient) {}

  getState(): Observable<StoryState> {
    return this.http.get<StoryState>(`${this.baseUrl}/state`);
  }

  choose(option: StoryOption): Observable<StoryState> {
    return this.http.post<StoryState>(`${this.baseUrl}/choice`, option);
  }
}
