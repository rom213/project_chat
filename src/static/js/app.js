import { createApp } from 'vue';
import Controls from './components/controls.vue';

const app = createApp({
  components: {
    Controls
  }
});

app.mount('#app2');
