import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Inventory } from '../../models';

@Component({
  selector: 'app-player-hud',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './player-hud.component.html',
  styleUrls: ['./player-hud.component.scss']
})
export class PlayerHudComponent {
  @Input() player: { stats: Record<string, number>; inventory: Inventory[] } | undefined;
  @Input() inventory: string[] = [];
  
  playerStatsArray() {
    return this.player ? Object.entries(this.player.stats).map(([name, value]) => ({ name, value })) : [];
  }
}
