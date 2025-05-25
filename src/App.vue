<template>
  <router-view />
</template>

<script setup>
import { useQuasar } from 'quasar'

const $q = useQuasar()
// get status
console.log($q.dark.isActive) // true, false
// set status
$q.dark.set(true) // or false or "auto"
// get configured status
console.log($q.dark.mode) // "auto", true, false
</script>
