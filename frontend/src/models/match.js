import Competitor from './competitor';

export default class Match {
  constructor(id, ordinal, competitor1, competitor2, competitor1Score, competitor2Score,
    nextMatchId, status) {
    this.id = id;
    this.ordinal = ordinal;
    this.competitor1 = competitor1;
    this.competitor2 = competitor2;
    this.competitor1Score = competitor1Score;
    this.competitor2Score = competitor2Score;
    this.nextMatchId = nextMatchId;
    this.status = status;
  }

  static fromCreateResponseBody(response) {
    return new Match(
      response.id,
      response.ordinal,
      Competitor.fromCreateResponseBody(response.competitor_1),
      Competitor.fromCreateResponseBody(response.competitor_2),
      response.competitor_1_score,
      response.competitor_2_score,
      response.next_match_id,
      response.status,
    );
  }
}
