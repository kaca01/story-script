import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlayerHudComponent } from './player-hud.component';

describe('PlayerHudComponent', () => {
  let component: PlayerHudComponent;
  let fixture: ComponentFixture<PlayerHudComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PlayerHudComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PlayerHudComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
