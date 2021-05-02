import Pool from '@/models/pool';

const TYPES = [
  { value: 0, text: 'Pool' },
  { value: 1, text: 'Single Elimination Bracket' },
  { value: 2, text: 'Double Elimination Bracket' },
];

export default class Stage {
  constructor(id, ordinal, type, status, params, pools) {
    this.id = id;
    this.ordinal = ordinal;
    this.type = type;
    this.status = status;
    this.params = params;
    this.pools = pools;
  }

  static get types() {
    return TYPES;
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
      response.pools.map((pool) => Pool.fromCreateResponseBody(pool)),
    );
  }
}
