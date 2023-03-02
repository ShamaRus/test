<template>
  <div>
    Статус выполнения задачи: {{ taskState }}<br>
    <button v-if="!taskId" @click="runTask">Запустить задачу</button>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
const TIMER_TIMEOUT = 1000


export default {
  name: 'TaskControl',
  data: () => ({
    timer: undefined,
  }),
  computed: {
    ...mapState('flights', ['taskId']),
    taskState() {
      return this.taskId ? 'Выполняется' : 'Не выполняется'
    }
  },
  watch: {
    taskId(value) {
      if (value && !this.timer) {
        this.timer = setTimeout(this.fetchTimer, TIMER_TIMEOUT);
      } else
      if (this.timer) {
        clearTimeout(this.timer)
        this.timer = undefined
      }
    }
  },
  mounted() {
    this.fetchTask()
  },
  methods: {
    ...mapActions('flights', ['fetchTask', 'runTask']),
    fetchTimer() {
      this.fetchTask()
      this.timer = setTimeout(this.fetchTimer, TIMER_TIMEOUT);
    },
  }
}
</script>

<style>
</style>
