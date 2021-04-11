import axios from 'axios';
import authHeader from '@/services/auth-header';
import Competitor from '@/models/competitor';

const API_URL = process.env.VUE_APP_API_URL;

class CompetitorService {
  static async createCompetitors(tournament, competitors) {
    const endpoint = `/tournaments/${tournament.id}/competitors/batch`;

    const response = await axios.post(
      API_URL + endpoint, competitors.map((competitor) => competitor.asCreateRequestBody()), {
        headers: authHeader(),
        validateStatus: (status) => status === 201,
      },
    );

    return response.data.map((competitor) => Competitor.fromCreateResponseBody(competitor));
  }

  static async updateCompetitors(tournament, competitors) {
    const endpoint = `/tournaments/${tournament.id}/competitors/`;

    const response = await axios.put(
      API_URL + endpoint, competitors.map((competitor) => competitor.asCreateRequestBody()), {
        headers: authHeader(),
        validateStatus: (status) => status === 200,
      },
    );

    return response.data.map((competitor) => Competitor.fromCreateResponseBody(competitor));
  }
}

export default CompetitorService;
