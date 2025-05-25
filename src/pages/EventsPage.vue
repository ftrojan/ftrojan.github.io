<template>
  <q-page class="column items-center q-gutter-md">
    <h5>Vystoupení</h5>
    <div class="column items-center q-gutter-md" style="width: 100%;">
      <q-card
        v-for="event in futureEvents"
        :key="event.id"
        class="q-mb-md"
        style="max-width: 800px; width: 100%;"
      >
        <q-card-section>
          <p>Kdy: {{ event.date }}</p>
          <p>Kde: {{ event.location }}</p>
          <img :src="photoUrl(event.poster_id)" style="height: 500px;" alt="Poster">
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script setup>
import { computed } from 'vue';
import data from 'src/assets/events.json';

const photoUrl = (fileId) => {
  const url = `https://lh3.googleusercontent.com/d/${fileId}`;
  return url;
};

const today = new Date();

const futureEvents = computed(() =>
  data.filter(event => new Date(event.date) >= today)
);
</script>
