import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { StoryService } from '../../../services/core/story.service';
import { StoryOption, StoryState } from '../../../models';

@Component({
  selector: 'app-story-view',
  standalone: true,
  imports: [CommonModule],
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

  selectOption(option: StoryOption): void {
    this.loading = true;

    // TODO: call service method
  }
}
