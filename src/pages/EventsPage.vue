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
        <q-card-section class="row items-start q-gutter-md">
          <div class="col">
            <h4 class="q-ma-none">{{ formatDate(event.date) }}</h4>
            <h5 class="q-ma-none q-mt-sm">{{ event.location }}</h5>
          </div>
          <div v-if="event.poster_id" class="poster-container">
            <img :src="photoUrl(event.poster_id)" style="height: 500px;" alt="Poster">
          </div>
          <div v-else class="poster-placeholder">
            {{ placeholderText }}
          </div>
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

const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  return new Intl.DateTimeFormat('cs-CZ', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  }).format(date);
};

const today = new Date();

const futureEvents = computed(() =>
  data.filter(event => new Date(event.date) >= today)
);

const placeholderText = "Plakát na tuto akci se připravuje";
</script>

<style scoped>
.poster-placeholder {
  height: 500px;
  width: 350px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  background-color: #310909;
  padding: 1rem;
  font-style: italic;
}
</style>
