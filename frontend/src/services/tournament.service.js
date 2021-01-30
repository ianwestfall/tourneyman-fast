import axios from 'axios';
import Tournament from '../models/tournament';
import User from '../models/user';
import authHeader from './auth-header';

const API_URL = process.env.VUE_APP_API_URL;

class TournamentService {
  static async getTournaments(isFilteredByUser, perPage, currentPage) {
    const endpoint = '/tournaments';

    const skip = (currentPage - 1) * perPage;
    const limit = perPage;

    const response = await axios.get(
      API_URL + endpoint, {
        params: {
          is_filtered_by_user: isFilteredByUser,
          skip,
          limit,
        },
        headers: authHeader(),
      },
    );
    const res = response.data;
    res.items = res.items.map((tournament) => new Tournament(
      tournament.id,
      tournament.name,
      tournament.organization,
      new Date(Date.parse(tournament.start_date)),
      tournament.public,
      tournament.status,
      new User(tournament.owner.email, null),
    ));

    return res;
  }
}

export default TournamentService;