import { Observable } from "rxjs";
import { StoryState } from "../../models";
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

  choose(option: number): Observable<StoryState> {
    console.log("Selected option index:", option);
    return this.http.post<StoryState>(`${this.baseUrl}/choice`, {optionIndex: option});
  }
}
