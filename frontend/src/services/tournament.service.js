import axios from 'axios';
import Tournament from '@/models/tournament';
import User from '@/models/user';
import authHeader from '@/services/auth-header';

const API_URL = process.env.VUE_APP_API_URL;

class TournamentService {
  static async getTournament(id) {
    const endpoint = `/tournaments/${id}`;

    const response = await axios.get(
      API_URL + endpoint, {
        headers: authHeader(),
        validateStatus: (status) => status === 200,
      },
    );

    return Tournament.fromCreateResponseBody(response.data);
  }

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
        validateStatus: (status) => status === 200,
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

  static async createTournament(tournament) {
    const endpoint = '/tournaments';

    const response = await axios.post(
      API_URL + endpoint, tournament.asCreateRequestBody(), {
        headers: authHeader(),
        validateStatus: (status) => status === 201,
      },
    );
    return Tournament.fromCreateResponseBody(response.data);
  }

  static async updateTournament(tournament) {
    const endpoint = `/tournaments/${tournament.id}`;

    const response = await axios.put(
      API_URL + endpoint, tournament.asCreateRequestBody(), {
        headers: authHeader(),
        validateStatus: (status) => status === 200,
      },
    );
    return Tournament.fromCreateResponseBody(response.data);
  }

  static async updateTournamentStatus(tournament, status) {
    const endpoint = `/tournaments/${tournament.id}/status`;

    const response = await axios.post(
      API_URL + endpoint, { status }, {
        headers: authHeader(),
        validateStatus: (statusCode) => statusCode === 201,
      },
    );

    return Tournament.fromCreateResponseBody(response.data);
  }
}

export default TournamentService;
