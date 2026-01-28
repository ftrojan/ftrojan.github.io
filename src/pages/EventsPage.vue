<template>
  <q-page class="column items-center q-gutter-md">
    <h5>Vystoupení</h5>
    <div class="column items-center q-gutter-md" style="width: 100%;">
      <q-card
        v-for="event in futureEvents"
        :key="event.date"
        class="q-mb-md event-card"
        style="width: 100%; min-height: 540px;"
      >
        <q-card-section class="row items-start justify-between full-width q-px-xl">
          <div class="event-info">
            <h4 class="q-ma-none">{{ formatDate(event.date) }} od {{ event.time }}</h4>
            <h5 class="q-ma-none q-mt-sm">{{ event.location }}</h5>
          </div>
          <div class="poster-wrapper">
            <div v-if="event.poster_id" class="poster-container">
              <img :src="photoUrl(event.poster_id)" style="height: 500px;" alt="Poster">
            </div>
            <div v-else class="poster-placeholder">
              {{ event.placeholderText ? event.placeholderText : placeholderText }}
            </div>
          </div>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script setup>
import { computed } from 'vue';
import data from 'src/assets/events.json';
import { formatDate, parseLocalDate } from 'src/utils/date';

const photoUrl = (fileId) => {
  //const url = `https://lh3.googleusercontent.com/d/${fileId}`;
  // const today = new Date().toISOString().split('T')[0]; // Gets YYYY-MM-DD
  // const imageUrl = `https://drive.google.com/uc?id=${fileId}&date=${today}`;
  const imageUrl = `https://lh3.googleusercontent.com/d/${fileId}`;
  return imageUrl;
};

// normalize "today" to local midnight
const today = new Date();
today.setHours(0, 0, 0, 0);

const futureEvents = computed(() =>
  data.filter(event => parseLocalDate(event.date) >= today)
);

const placeholderText = "Plakát na tuto akci se připravuje";
</script>

<style scoped>
.poster-wrapper {
  margin-left: auto;
}

.poster-container {
  margin-left: auto;
  height: 500px;
  width: 350px;
  display: flex;
  align-items: right;
  justify-content: center;
}

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

.event-card {
  display: flex;
  align-items: stretch;
}

.event-info {
  flex: 1;
  padding-right: 2rem;
}
</style>
