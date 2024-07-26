<template>
    <div class="bg-blue-50 w-full h-full absolute -left-3 rounded-2xl pt-16 overflow-x-auto">
      <h1>Control Component</h1>
      <input v-model="input" type="text" />
      <div>{{ input }}</div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const input = ref("romasr");
  </script>