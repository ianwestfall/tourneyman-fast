export default class Competitor {
  constructor(id, firstName, lastName, organization, location) {
    this.id = id;
    this.firstName = firstName;
    this.lastName = lastName;
    this.organization = organization;
    this.location = location;
  }

  asCreateRequestBody() {
    return {
      first_name: this.firstName,
      last_name: this.lastName,
      organization: this.organization,
      location: this.location,
    };
  }

  static fromCreateResponseBody(response) {
    return new Competitor(
      response.id,
      response.first_name,
      response.last_name,
      response.organization,
      response.location,
    );
  }
}
