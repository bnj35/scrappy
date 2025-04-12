<script setup>
defineProps({
  title: String,
  link: String,
})
</script>

<template>
  <div class="card">
    <h3>{{ title }}</h3>
    <a :href="link" target="_blank" rel="noopener noreferrer">Voir l'offre</a>
  </div>
</template>

<style scoped>
.card {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 16px;
  margin: 8px 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
.card h3 {
  margin: 0 0 8px;
  font-size: 18px;
}
.card a {
  color: #007bff;
  text-decoration: none;
}
.card a:hover {
  text-decoration: underline;
}
</style>