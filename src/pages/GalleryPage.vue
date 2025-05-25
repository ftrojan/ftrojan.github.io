<template>
  <q-page class="column items-center q-gutter-md">
    <h5>Galerie</h5>
    <div class="column items-center q-gutter-md" style="width: 100%;">
      <q-card
        v-for="event in pastEvents"
        :key="getId(event.date)"
        class="q-mb-md"
        style="max-width: 1000px; width: 100%;"
      >
        <q-card-section>
          <p>Kdy: {{ event.date }}</p>
          <p>Kde: {{ event.location }}</p>
          <q-carousel
            v-if="event.gallery && event.gallery.length > 0"
            :model-value="getMediaIndex(getId(event.date))"
            @update:model-value="val => setMediaIndex(getId(event.date), val)"
            :fullscreen="getFullscreen(getId(event.date))"
            @update:fullscreen="val => setFullscreen(getId(event.date), val)"
            swipeable
            animated
            arrows
            style="min-width: 1000px;"
          >
            <q-carousel-slide
              v-for="(media, index) in event.gallery"
              :key="index"
              :name="index"
            >
              <q-video
                v-if="media.type === 'video'"
                :src="videoUrl(media.id)"
                :poster="photoUrl(media.poster_id)"
                controls
                style="width: 100%; height: 500px;"
              />
              <q-img
                v-else-if="media.type === 'image'"
                :src="photoUrl(media.id)"
                style="width: 100%; height: 500px;"
                alt="Gallery Image"
              />
            </q-carousel-slide>
            <q-carousel-control
              position="bottom-right"
              color="white"
              text-color="black"
              :icon="event.gallery.length > 1 ? 'chevron_right' : ''"
            />
            <q-carousel-control
              position="bottom-left"
              color="white"
              text-color="black"
              :icon="event.gallery.length > 1 ? 'chevron_left' : ''"
            />
            <template v-slot:control>
              <q-carousel-control
                position="bottom-right"
                :offset="[18, 18]"
              >
                <q-btn
                  push round dense color="white" text-color="primary"
                  :icon="getFullscreen(getId(event.date)) ? 'fullscreen_exit' : 'fullscreen'"
                  @click="setFullscreen(getId(event.date), !getFullscreen(getId(event.date)))"
                />
              </q-carousel-control>
            </template>
          </q-carousel>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script setup>
import { computed, ref } from 'vue';
import data from 'src/assets/events.json';

const photoUrl = (fileId) => `https://lh3.googleusercontent.com/d/${fileId}`;
const videoUrl = (fileId) => `https://www.youtube.com/embed/${fileId}`;
const getId = (eventDate) => parseInt(eventDate.replaceAll('-', ''), 10);

const today = new Date();

const pastEvents = computed(() =>
  data
    .filter(event => new Date(event.date) < today)
    .sort((a, b) => new Date(b.date) - new Date(a.date))
);

// Per-event state
const mediaIndexes = ref({});
const fullscreens = ref({});

const getMediaIndex = (eventId) => mediaIndexes.value[eventId] ?? 0;
const setMediaIndex = (eventId, val) => { mediaIndexes.value[eventId] = val; };

const getFullscreen = (eventId) => fullscreens.value[eventId] ?? false;
const setFullscreen = (eventId, val) => { fullscreens.value[eventId] = val; };
</script>
