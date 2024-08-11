<template>
  <div class="container"><h1><a class="header-link" href="/">Blockchain Explorer</a></h1>
    <div>
      <table>
        <thead>
        <tr>
          <th>#</th>
          <th>hash</th>
          <th>Transactions</th>
          <th>Timestamp</th>
        </tr>
        </thead>

        <tbody>
        <tr v-for="block in blocks">
          <td>{{ block.block_height }}</td>
          <td><router-link :to="{ name: 'Block', params: { id: block.block_height }}">{{ block.signature }}</router-link></td>
          <td>{{ block.transactions.length }}</td>
          <td>{{ block.timestamp}}</td>
        </tr>
        </tbody>
      </table>
    </div>
</div>

</template>

<script>
  export default {
    name: 'FrontPage',
    data() {
      return {
        blocks: [],
        peers :[]

      }
    },
    created() {
      this.getBlocks();
      this.getPeers();
    },
    methods: {
      getBlocks: function () {
        this.$http.get('http://localhost:9050/api/v1/blockchain/')
          .then((resp) => {
            this.blocks = resp.data.blocks;
            this.blocks = sortBlocks(this.blocks)
          })
      },

      sortBlocks : function(blocks) {
        return _(blocks)
          .sortBy('block_height')
          .reverse()
          .value();
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
