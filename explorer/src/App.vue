<template>
  <div id="app">
    <ul>
      <li> <router-link :to="{ name: 'FrontPage'}">Home</router-link> </li>
      <li> <router-link :to="{ name: 'Validators'}">Validators</router-link> </li>
      <li class="right"> <router-link :to="{ name: 'Mempool'}">Pending Transactions</router-link> </li>
    </ul>

      <router-view class="app_container" :key="$route.fullPath"/>

      </div>
</template>

<script>
export default {
  name: 'app',
  created()
  {

  },
}
</script>

<style>
body{
  margin: 0;
}

.header-link {
  color: black;
  text-decoration: none; /* no underline */
}

.break-word {
  word-wrap: break-word;
}
ul {
  list-style-type: none;
  margin: 0;
  padding: 1% 2%;
  overflow: hidden;
  background-color: #333;
}

li {
  float: left;
}

li a {
  display: block;
  color: white;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
}
li.right {float: right;}

/* Change the link color to #111 (black) on hover */
li a:hover {
  background-color: #111;
}

.app_container{
  padding: 2% 10%;
}

</style>
