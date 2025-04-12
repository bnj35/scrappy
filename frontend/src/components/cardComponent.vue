<script setup>
defineProps({
  title: String,
  company: String,
  location: String,
  contract: String,
  date: String,
  duration: String,
  link: String,
})
</script>

<template>
  <div class="card">
    <h3>{{ title }}</h3>
    <p><strong>Entreprise:</strong> {{ company }}</p>
    <p><strong>Lieu:</strong> {{ location }}</p>
    <p><strong>Contrat:</strong> {{ contract }}</p>
    <p v-if="duration"><strong>Durée:</strong> {{ duration }}</p>
    <p v-if="date"><strong>Date de publication:</strong> {{ date }}</p>
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
.card p {
  margin: 4px 0;
  font-size: 14px;
}
.card a {
  color: #007bff;
  text-decoration: none;
}
.card a:hover {
  text-decoration: underline;
}
</style>