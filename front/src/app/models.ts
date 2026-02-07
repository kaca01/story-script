export interface StoryState {
  header: string;
  body: string;
  imagePath: string;
  options: StoryOption[];
  player?: PlayerStats;
}

export interface PlayerStats {
  stats: Record<string, number>;
  inventory: string[];
}

export interface StoryOption {
  text: string;
  room: string;
  action: StoryAction | null;
}

export interface StoryAction {
  take?: string;
  assignments: Assignment[];
  rules: any[];
}

export interface Assignment {
  varName: string;
  exp: Record<string, number>;
}
