export default function authHeader() {
  const userToken = JSON.parse(localStorage.getItem('userToken'));
  let headers = {};

  if (userToken && userToken.access_token) {
    headers = { Authorization: `Bearer ${userToken.access_token}` };
  }

  return headers;
}
