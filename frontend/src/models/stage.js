const TYPES = [
  { value: 0, text: 'Pool' },
  { value: 1, text: 'Single Elimination Bracket' },
  { value: 2, text: 'Double Elimination Bracket' },
];

export default class Stage {
  constructor(id, ordinal, type, status) {
    this.id = id;
    this.ordinal = ordinal;
    this.type = type;
    this.status = status;
  }

  static get types() {
    return TYPES;
  }

  static parse(stage) {
    return new Stage(stage.id, stage.ordinal, stage.type, stage.status);
  }
}
