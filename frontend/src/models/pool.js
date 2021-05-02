import Match from '@/models/match';

export default class Pool {
  constructor(id, ordinal, matches) {
    this.id = id;
    this.ordinal = ordinal;
    this.matches = matches;
  }

  static fromCreateResponseBody(response) {
    return new Pool(
      response.id,
      response.ordinal,
      response.matches.map((match) => Match.fromCreateResponseBody(match)),
    );
  }
}
