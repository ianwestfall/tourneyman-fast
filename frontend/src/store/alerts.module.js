const typeMap = {
  error: 'danger',
  info: 'info',
};
const initialState = { alerts: [] };

export default {
  namespaced: true,
  state: initialState,
  actions: {
    raiseError({ commit }, message) {
      commit('raiseAlert', { type: typeMap.error, message });
    },
    raiseInfo({ commit }, message) {
      commit('raiseAlert', { type: typeMap.info, message });
    },
  },
  mutations: {
    raiseAlert(state, payload) {
      const { type, message } = payload;
      switch (type) {
        case typeMap.error:
          state.alerts.push({ type, message });
          break;
        case typeMap.info:
          state.alerts.push({ type, message });
          break;
        default:
          break;
      }
    },
  },
  getters: {
    getAlerts: (state) => state.alerts,
  },
};
