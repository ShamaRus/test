export default {
  async fetchTask({ commit, state }) {
    const res = await this.$axios.get("/task", {params: {
      task_id: state.taskId
      }})
    if (res.data) {
      commit('setTaskId', res.data.status !== "SUCCESS" && res.data.id || null)
    }
    return res.data;
  },
  async runTask({ commit }) {
    const res = await this.$axios.post("/task")
    commit('setTaskId', res.data)
    return res.data;
  },
  async fetchFlights({ commit }) {
    const res = await this.$axios.get("/flights")
    commit('setFlights', res.data)
    return res.data;
  },
}
