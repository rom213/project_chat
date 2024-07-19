


<script>
const { ref } = Vue;

const app = {
    setup() {
        const showSidebar = ref(true);

        const toggleSidebar = () => {
            showSidebar.value = !showSidebar.value;
        };

        return {
            showSidebar,
            toggleSidebar
        };
    }
};

Vue.createApp(app).mount('#sidebar-app');
</script>