import { expect } from 'chai';
import AuthService from '@/services/auth.service';
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import User from '@/models/user';

const API_URL = process.env.VUE_APP_API_URL;

describe('auth service', () => {
  let mockApi;

  before(() => {
    mockApi = new MockAdapter(axios);
  });

  beforeEach(() => {
    // Make sure localStorage is empty.
    window.localStorage.clear();
  });

  afterEach(() => {
    mockApi.reset();

    // Clean up any staged data from localStorage
    window.localStorage.clear();
  });

  after(() => {
    mockApi.restore();
  });

  describe('login()', () => {
    it('raises an exception when user is null', async () => {
      // undefined user
      try {
        await AuthService.login();
        expect.fail('login should have raised an exception');
      } catch (error) {
        expect(error).to.be.an.instanceOf(TypeError);
        expect(error.message).to.eql('user must not be null/undefined');
      }

      // null user
      try {
        await AuthService.login(null);
        expect.fail('login should have raised an exception');
      } catch (error) {
        expect(error).to.be.an.instanceOf(TypeError);
        expect(error.message).to.eql('user must not be null/undefined');
      }

      expect(mockApi.history.post.length).to.eql(0);
    });

    it('raises an exception when user is mis-formatted', async () => {
      // missing email
      try {
        await AuthService.login({ password: 'p' });
        expect.fail('login should have raised an exception');
      } catch (error) {
        expect(error).to.be.an.instanceOf(TypeError);
        expect(error.message).to.eql('user must have an email and a password');
      }

      // missing password
      try {
        await AuthService.login({ email: 'e' });
        expect.fail('login should have raised an exception');
      } catch (error) {
        expect(error).to.be.an.instanceOf(TypeError);
        expect(error.message).to.eql('user must have an email and a password');
      }

      // empty email
      try {
        await AuthService.login({ email: '', password: 'p' });
        expect.fail('login should have raised an exception');
      } catch (error) {
        expect(error).to.be.an.instanceOf(TypeError);
        expect(error.message).to.eql('user must have an email and a password');
      }

      // empty password
      try {
        await AuthService.login({ email: 'e', password: '' });
        expect.fail('login should have raised an exception');
      } catch (error) {
        expect(error).to.be.an.instanceOf(TypeError);
        expect(error.message).to.eql('user must have an email and a password');
      }

      expect(mockApi.history.post.length).to.eql(0);
    });

    it('raises an exception when the login post fails', async () => {
      mockApi.onPost(`${API_URL}/auth/token`).networkError();

      try {
        await AuthService.login({ email: 'test@test.com', password: 'password' });
        expect.fail('login should have raised an exception');
      } catch (error) {
        expect(error.message).to.eql('Network Error');
      }

      // Make sure the request body was correct
      expect(mockApi.history.post.length).to.eql(1);
      expect(mockApi.history.post[0].data).to.be.an.instanceOf(FormData);
      expect(mockApi.history.post[0].data.get('username')).to.eql('test@test.com');
      expect(mockApi.history.post[0].data.get('password')).to.eql('password');
    });

    it('does not store the user token if it is not present', async () => {
      mockApi.onPost(`${API_URL}/auth/token`).reply(200, {});

      const responseData = await AuthService.login({ email: 'test@test.com', password: 'password' });
      expect(responseData).to.eql({});
      expect(window.localStorage.getItem('user')).to.be.null;
      expect(window.localStorage.getItem('userToken')).to.be.null;

      // Make sure the request body was correct
      expect(mockApi.history.post.length).to.eql(1);
      expect(mockApi.history.post[0].data).to.be.instanceOf(FormData);
      expect(mockApi.history.post[0].data.get('username')).to.eql('test@test.com');
      expect(mockApi.history.post[0].data.get('password')).to.eql('password');
    });

    it('stores the user token if login was successful', async () => {
      const testResponseData = { access_token: 'test_access_token' };
      mockApi.onPost(`${API_URL}/auth/token`).reply(200, testResponseData);

      const responseData = await AuthService.login({ email: 'test@test.com', password: 'password' });
      expect(responseData).to.eql(testResponseData);
      expect(window.localStorage.getItem('user')).to.eql(JSON.stringify(new User('test@test.com')));
      expect(window.localStorage.getItem('userToken')).to.eql(JSON.stringify(testResponseData));

      // Make sure the request body was correct
      expect(mockApi.history.post.length).to.eql(1);
      expect(mockApi.history.post[0].data).to.be.instanceOf(FormData);
      expect(mockApi.history.post[0].data.get('username')).to.eql('test@test.com');
      expect(mockApi.history.post[0].data.get('password')).to.eql('password');
    });
  });

  describe('logout()', () => {
    it('is a no-op if there is no logged in user', () => {
      AuthService.logout();

      expect(window.localStorage.getItem('user')).to.be.null;
      expect(window.localStorage.getItem('userToken')).to.be.null;
    });

    it('clears the user token if there is a logged in user', () => {
      window.localStorage.setItem('user', JSON.stringify(new User('test@test.com')));
      window.localStorage.setItem('userToken', JSON.stringify({ access_token: 'test_acces_token' }));

      AuthService.logout();

      expect(window.localStorage.getItem('user')).to.be.null;
      expect(window.localStorage.getItem('userToken')).to.be.null;
    });
  });

  describe('register()', () => {
    it('raises an exception when user is null', async () => {
      // undefined user
      try {
        await AuthService.register();
        expect.fail('register should have raised an exception');
      } catch (error) {
        expect(error).to.be.an.instanceOf(TypeError);
        expect(error.message).to.eql('user must not be null/undefined');
      }

      // null user
      try {
        await AuthService.register(null);
        expect.fail('register should have raised an exception');
      } catch (error) {
        expect(error).to.be.an.instanceOf(TypeError);
        expect(error.message).to.eql('user must not be null/undefined');
      }

      expect(mockApi.history.post.length).to.eql(0);
    });

    it('raises an exception when user is mis-formatted', async () => {
      // missing email
      try {
        await AuthService.register({ password: 'p' });
        expect.fail('register should have raised an exception');
      } catch (error) {
        expect(error).to.be.an.instanceOf(TypeError);
        expect(error.message).to.eql('user must have an email and a password');
      }

      // missing password
      try {
        await AuthService.register({ email: 'e' });
        expect.fail('register should have raised an exception');
      } catch (error) {
        expect(error).to.be.an.instanceOf(TypeError);
        expect(error.message).to.eql('user must have an email and a password');
      }

      // empty email
      try {
        await AuthService.register({ email: '', password: 'p' });
        expect.fail('register should have raised an exception');
      } catch (error) {
        expect(error).to.be.an.instanceOf(TypeError);
        expect(error.message).to.eql('user must have an email and a password');
      }

      // empty password
      try {
        await AuthService.register({ email: 'e', password: '' });
        expect.fail('register should have raised an exception');
      } catch (error) {
        expect(error).to.be.an.instanceOf(TypeError);
        expect(error.message).to.eql('user must have an email and a password');
      }

      expect(mockApi.history.post.length).to.eql(0);
    });

    it('calls the register endpoint correctly', async () => {
      mockApi.onPost(`${API_URL}/auth/users`).reply(201, {});

      await AuthService.register({ email: 'test@test.com', password: 'password' });

      expect(mockApi.history.post.length).to.eql(1);
      expect(mockApi.history.post[0].data).to.eql(JSON.stringify({ email: 'test@test.com', password: 'password' }));
    });

    it('raises an exception if the login call fails', async () => {
      mockApi.onPost(`${API_URL}/auth/users`).networkError();

      try {
        await AuthService.register({ email: 'test@test.com', password: 'password' });
        expect.fail('register should have raised an exception');
      } catch (error) {
        expect(error.message).to.eql('Network Error');
      }

      expect(mockApi.history.post.length).to.eql(1);
      expect(mockApi.history.post[0].data).to.eql(JSON.stringify({ email: 'test@test.com', password: 'password' }));
    });
  });
});
