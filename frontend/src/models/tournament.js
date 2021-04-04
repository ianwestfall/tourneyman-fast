import Stage from '@/models/stage';
import Competitor from './competitor';

export default class Tournament {
  constructor(id, name, organization, startDate, pub, status, owner,
    stages, competitors) {
    this.id = id;
    this.name = name;
    this.organization = organization;
    this.startDate = startDate;
    this.public = !!pub;
    this.status = status;
    this.owner = owner;
    this.stages = stages;
    this.competitors = competitors;
  }

  static convertStatusCode(status) {
    const statuses = {
      0: 'Pending',
      1: 'Ready',
      2: 'Active',
      3: 'Complete',
    };

    let convertedStatus;
    if (status in statuses) {
      convertedStatus = statuses[status];
    } else {
      convertedStatus = status;
    }

    return convertedStatus;
  }

  asCreateRequestBody() {
    return {
      name: this.name,
      organization: this.organization,
      start_date: this.startDate.toISOString(),
      public: this.public,
    };
  }

  static fromCreateResponseBody(response) {
    return new Tournament(
      response.id,
      response.name,
      response.organization,
      new Date(response.start_date),
      response.public,
      response.status,
      response.owner,
      response.stages.map((stage) => Stage.fromCreateResponseBody(stage)),
      response.competitors.map((competitor) => Competitor.fromCreateResponseBody(competitor)),
    );
  }
}
