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
}
