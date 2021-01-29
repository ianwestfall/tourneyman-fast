import axios from 'axios';
import Tournament from '../models/tournament';
import User from '../models/user';
import authHeader from './auth-header';

const API_URL = process.env.VUE_APP_API_URL;

class TournamentService {
  static async getTournaments() {
    const endpoint = '/tournaments';

    const response = await axios.get(API_URL + endpoint, { headers: authHeader() });

    return response.data.map((tournament) => new Tournament(
      tournament.id,
      tournament.name,
      tournament.organization,
      new Date(Date.parse(tournament.start_date)),
      tournament.public,
      tournament.status,
      new User(tournament.owner.email, null),
    ));
  }
}

export default TournamentService;
