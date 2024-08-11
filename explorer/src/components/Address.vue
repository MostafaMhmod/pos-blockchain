<template>
  <div>
    <div class="container"><h3>Address: {{$route.params.address}}</h3>  </div>
    <div class="container"><h3>Balance: {{balance}}</h3>  </div>

    <h3>Transactions:</h3>

    <div class="transaction" v-for="transaction in transactions">
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
    name: 'Transaction',
    data() {
      return {
        balance: 0,
        transactions :[]
      }
    },
    created() {
      this.getAddressBalance(this.$route.params.address)
      this.getAddressTransactions(this.$route.params.address)
    },
    methods: {
      getAddressBalance: function (address) {
        this.$http.get('http://localhost:9050/api/v1/transaction/' + address + "/balance/")
          .then(resp => {
            this.balance = resp.data;
          })
      },
      getAddressTransactions: function (address) {
        this.$http.get('http://localhost:9050/api/v1/transaction/' + address + "/transactions/")
          .then(resp => {
            this.transactions = resp.data;
          })
      },
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
.transaction{
  max-width: 80%;
}

</style>
