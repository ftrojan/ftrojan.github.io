<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar class="bg-black text-white">
        <q-btn flat dense icon="menu" to="/" />
        <q-btn
          style="background: #0e577b; color: white"
          class="q-mx-xs q-px-md"
          flat
          dense
          label="Bio"
          to="/bio"
        />
        <q-btn
          style="background: #0e577b; color: white"
          class="q-mx-xs q-px-md"
          flat
          dense
          label="Vystoupení"
          to="/events"
        />
        <q-btn
          style="background: #0e577b; color: white"
          class="q-mx-xs q-px-md"
          flat
          dense
          label="Galerie"
          to="/gallery"
        />
        <q-btn
          style="background: #0e577b; color: white"
          class="q-mx-xs q-px-md"
          flat
          dense
          label="Kontakt"
          to="/contact"
        />

        <q-toolbar-title class="q-mx-md"> Orion Jazz Band </q-toolbar-title>
      </q-toolbar>
    </q-header>
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup></script>
