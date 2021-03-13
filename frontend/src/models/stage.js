const TYPES = [
  { value: 0, text: 'Pool' },
  { value: 1, text: 'Single Elimination Bracket' },
  { value: 2, text: 'Double Elimination Bracket' },
];

export default class Stage {
  constructor(id, ordinal, type, status, params) {
    this.id = id;
    this.ordinal = ordinal;
    this.type = type;
    this.status = status;
    this.params = params;
  }

  static get types() {
    return TYPES;
  }

  static parse(stage) {
    return new Stage(stage.id, stage.ordinal, stage.type, stage.status, stage.params);
  }

  asCreateRequestBody() {
    return {
      type: this.type,
      params: this.params,
    };
  }

  static fromCreateResponseBody(response) {
    return new Stage(
      response.id,
      response.ordinal,
      response.type,
      response.status,
      response.params,
    );
  }
}
