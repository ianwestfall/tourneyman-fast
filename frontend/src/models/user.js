export default class User {
  constructor(email, password) {
    this.email = email;
    this.password = password;
  }

  getUsername() {
    return this.email.substr(0, this.email.indexOf('@'));
  }
}
