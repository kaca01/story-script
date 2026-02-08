export interface StoryState {
  header: string;
  body: string;
  imagePath: string;
  options: StoryOption[];
  player?: PlayerStats;
}

export interface PlayerStats {
  stats: Record<string, number>;
  inventory: Inventory[];
}

export interface Inventory {
  name: string;
  hp: number;
}

export interface StoryOption {
  text: string;
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
