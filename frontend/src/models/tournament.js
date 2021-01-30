export default class Tournament {
  constructor(id, name, organization, startDate, pub, status, owner) {
    this.id = id;
    this.name = name;
    this.organization = organization;
    this.startDate = startDate;
    this.public = pub;
    this.status = status;
    this.owner = owner;
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
}