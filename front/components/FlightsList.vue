<template>
  <div>
    <button @click="fetchFlights">Получить данные</button>
    <table>
      <tr>
        <th>hex</th>
        <th>reg_number</th>
        <th>flag</th>
        <th>lat</th>
        <th>lng</th>
        <th>alt</th>
        <th>dir</th>
        <th>speed</th>
        <th>v_speed</th>
        <th>squawk</th>
        <th>airline_icao</th>
        <th>airline_iata</th>
        <th>aircraft_icao</th>
        <th>flight_icao</th>
        <th>flight_iata</th>
        <th>flight_number</th>
        <th>dep_icao</th>
        <th>dep_iata</th>
        <th>arr_icao</th>
        <th>arr_iata</th>
        <th>updated</th>
        <th>status</th>
      </tr>
      <tr v-for="(flight, i) in flights" :key="i">
        <td>{{ flight.hex }}</td>
        <td>{{ flight.reg_number }}</td>
        <td>{{ flight.flag }}</td>
        <td>{{ flight.lat }}</td>
        <td>{{ flight.lng }}</td>
        <td>{{ flight.alt }}</td>
        <td>{{ flight.dir }}</td>
        <td>{{ flight.speed }}</td>
        <td>{{ flight.v_speed }}</td>
        <td>{{ flight.squawk }}</td>
        <td>{{ flight.airline_icao }}</td>
        <td>{{ flight.airline_iata }}</td>
        <td>{{ flight.aircraft_icao }}</td>
        <td>{{ flight.flight_icao }}</td>
        <td>{{ flight.flight_iata }}</td>
        <td>{{ flight.flight_number }}</td>
        <td>{{ flight.dep_icao }}</td>
        <td>{{ flight.dep_iata }}</td>
        <td>{{ flight.arr_icao }}</td>
        <td>{{ flight.arr_iata }}</td>
        <td>{{ flight.updated }}</td>
        <td>{{ flight.status }}</td>
      </tr>
    </table>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'


export default {
  name: 'FlightsList',
  data: () => ({
    timer: undefined,
  }),
  computed: {
    ...mapState('flights', ['flights']),
  },
  mounted() {
    this.fetchFlights()
  },
  methods: {
    ...mapActions('flights', ['fetchFlights']),
  }
}
</script>

<style scoped>
  table,
  table td {
      border: 1px solid black;
  }

  table {
    margin-top: 10px;
  }
</style>
