import { expect } from 'chai';
import authHeader from '@/services/auth-header';

describe('auth-header service', () => {
  beforeEach(() => {
    // Make sure localStorage is empty.
    window.localStorage.clear();
  });

  afterEach(() => {
    // Clean up any staged data from localStorage
    window.localStorage.clear();
  });

  it('returns no header when no user token is present', () => {
    // No userToken in localStorage
    let headers = authHeader();
    expect(headers).to.eql({});

    // Null userToken in localStorage
    window.localStorage.setItem('userToken', null);
    headers = authHeader();
    expect(headers).to.eql({});
  });

  it('returns no header when no access token is present', () => {
    // No access_token within the userToken
    window.localStorage.setItem('userToken', JSON.stringify({}));
    let headers = authHeader();
    expect(headers).to.eql({});

    // Null access_token within the userToken
    window.localStorage.setItem('userToken', JSON.stringify({ access_token: null }));
    headers = authHeader();
    expect(headers).to.eql({});
  });

  it('returns an Authorization header when the user is authenticated', () => {
    const testAccessToken = 'test_access_token';
    window.localStorage.setItem('userToken', JSON.stringify({ access_token: testAccessToken }));
    const headers = authHeader();
    expect(headers).to.eql({ Authorization: `Bearer ${testAccessToken}` });
  });
});
