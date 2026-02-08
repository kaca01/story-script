import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StoryService } from '../../../services/core/story.service';
import { StoryState } from '../../../models';
import { PlayerHudComponent } from "../../player-hud/player-hud.component";

@Component({
  selector: 'app-story-view',
  standalone: true,
  imports: [CommonModule, PlayerHudComponent],
  templateUrl: './story-view.component.html',
  styleUrls: ['./story-view.component.scss']
})
export class StoryViewComponent implements OnInit {
  state?: StoryState;
  loading = false;

  constructor(private storyService: StoryService) {}

  ngOnInit(): void {
    this.loadState();
  }

  loadState(): void {
    this.loading = true;
    this.storyService.getState().subscribe({
      next: (state) => {
        this.state = state;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      }
    });
  }

  selectOption(option: number): void {
    this.loading = true;

     this.storyService.choose(option).subscribe({
      next: (state) => {
        this.state = state;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      }
    });
  }
}
