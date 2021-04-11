import axios from 'axios';
import authHeader from '@/services/auth-header';
import Stage from '@/models/stage';

const API_URL = process.env.VUE_APP_API_URL;

class StageService {
  static async createStages(tournament, stages) {
    const endpoint = `/tournaments/${tournament.id}/stages`;

    const response = await axios.post(
      API_URL + endpoint, stages.map((stage) => stage.asCreateRequestBody()), {
        headers: authHeader(),
        validateStatus: (status) => status === 201,
      },
    );

    return response.data.map((stage) => Stage.fromCreateResponseBody(stage));
  }

  static async updateStages(tournament, stages) {
    const endpoint = `/tournaments/${tournament.id}/stages/`;

    const response = await axios.put(
      API_URL + endpoint, stages.map((stage) => stage.asCreateRequestBody()), {
        headers: authHeader(),
        validateStatus: (status) => status === 200,
      },
    );

    return response.data.map((stage) => Stage.fromCreateResponseBody(stage));
  }
}

export default StageService;
