<template>
  <div v-if="block.signature">

    <h3>Block #{{ block.block_height }}</h3>
    <table>
      <tbody>
      <tr>
        <td>Creator</td>
        <td><router-link :to="{ name: 'Address', params: { address: block.forger }}"> <span >{{ block.forger }}</span></router-link></td>

      </tr>
      <tr>
        <td>Hash</td>
        <td>{{ block.signature }}</td>
      </tr>
      <tr>
        <td>Previous hash</td>
        <td>{{ block.last_hash}}</td>
      </tr>
      <tr>
        <td>Timestamp</td>
        <td>{{ block.timestamp}}</td>
      </tr>
      <tr>
        <td>Number of transactions</td>
        <td>{{ block.transactions.length}}</td>
      </tr>

      </tbody>
    </table>
    <h3>Transactions:</h3>
    <div class="transaction" v-for="transaction in block.transactions">

      <table>
      <tbody>
        <tr>
        <td>Hash</td>
        <td><router-link :to="{ name: 'Transaction', params: { id: transaction.signature }}"> <span >{{ transaction.signature }}</span></router-link></td>
      </tr>
      <tr>
        <td>From</td>
        <td v-if="transaction.sender_public_key == 'COINBASE'">{{ transaction.sender_public_key}}</td>
        <td v-else><router-link  :to="{ name: 'Address', params: { address: transaction.sender_public_key }}"> <span >{{ transaction.sender_public_key }}</span></router-link></td>
      </tr>
      <tr>
        <td>To</td>
        <td><router-link :to="{ name: 'Address', params: { address: transaction.receiver_public_key }}"> <span >{{ transaction.receiver_public_key }}</span></router-link></td>
      </tr>
      <tr>
        <td>Amount</td>
        <td>{{ transaction.amount}}</td>
      </tr>

      </tbody>
    </table>

    </div>
  </div>
</template>

<script>
  export default {
    name: 'Block',
    data() {
      return {
        block :{}
      }
    },
    created() {
      this.getBlock(this.$route.params.id)
    },
    methods: {
      getBlock: function (hash) {
        this.$http.get('http://localhost:9050/api/v1/blockchain/block/' + hash)
          .then(resp => {
            this.block = resp.data;
          })
      },
      trimAddress: function(address) {
        return address.substr(0,24) + '...';
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

.transaction {
    padding: 1em;
    margin-bottom: 1em;
    background-color: gainsboro;
  }
.tx{
  max-width: 80%;
}
</style>
