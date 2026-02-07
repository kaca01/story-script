export interface StoryState {
  header: string;
  body: string;
  imagePath: string;
  options: StoryOption[];
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
