<template>
  <div>
    <div class="container"><h3>Validators:</h3>  </div>
      <table>
        <thead>
        <tr>
          <th>Name</th>
          <th>ip</th>
          <th>Port</th>
        </tr>
        </thead>

        <tbody>
        <tr v-for="peer in peers">
          <td>{{ peer.docker_ip }}</td>
          <td>{{ peer.ip }}</td>
          <td>{{ peer.port}}</td>
        </tr>
        </tbody>
      </table>
    </div>

</template>

<script>
  export default {
    name: 'Validators',
    data() {
      return {
        peers :[]

      }
    },
    created() {
      this.getPeers();
    },
    methods: {
      getPeers: function () {
        this.$http.get('http://localhost:9050/api/v1/blockchain/peers/')
          .then(resp => {
            this.peers = resp.data;
          })
      }
    }
  }
</script>


<style scoped>
.table-container {
  width: 100%;
  overflow-x: auto; /* Ensure the table can scroll horizontally if necessary */
}

table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed; /* Ensures equal width for all columns */
}

th, td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
  white-space: nowrap; /* Prevents text from wrapping */
  overflow: hidden; /* Ensures content that overflows is hidden */
  text-overflow: ellipsis; /* Shows ellipsis (...) for overflowed content */
}

th {
  background-color: #f4f4f4;
}
</style>
