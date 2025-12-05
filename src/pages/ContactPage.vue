<template>
  <q-page class="column q-mx-xs q-px-md">
    <p class="text-h6 q-mt-md">Filip Trojan</p>
    <p>Telefon: +420 733 598 521</p>
    <p>WhatsApp: viz telefon</p>
    <p>Email: filip.trojan@proton.me</p>
    <p>Facebook: <a href="https://www.facebook.com/orionjazzband">https://www.facebook.com/orionjazzband</a></p>
    <p>Songbook: <a href="https://github.com/ftrojan/songbook/tree/main/pdf">https://github.com/ftrojan/songbook/tree/main/pdf</a></p>
    <h3>Pro pořadatele - stage plan</h3>
    <div class="stage-plan-wrapper">
      <img
        src="https://lh3.googleusercontent.com/d/1NLjoFzmHZLC9h2UnFl8BO359K08hnCP7"
        alt="Stage plan"
        class="stage-plan-img"
      />
    </div>
  </q-page>
</template>

<script setup></script>

<style scoped>
.stage-plan-wrapper {
  display: inline-block;      /* do not stretch in flex column */
  align-self: flex-start;     /* keep at left and intrinsic size */
  margin-bottom: 16px;
}

.stage-plan-img {
  display: block;
  width: auto !important;
  height: auto !important;
  max-width: none !important;
  max-height: none !important;
  object-fit: none !important;
}
</style>
