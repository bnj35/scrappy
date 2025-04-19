<script setup>
import { ref } from 'vue'

defineProps({
  title: String,
  company: String,
  location: String,
  contract: String,
  date: String,
  duration: String,
  link: String,
})

defineEmits(['generateLetter'])

const selectedTemplate = ref('alternance')

</script>

<template>
  <div class="card">
    <h3>{{ title }}</h3>
    <p><strong>Entreprise:</strong> {{ company }}</p>
    <p v-if="location"><strong>Lieu:</strong> {{ location }}</p>
    <p v-if="contract"><strong>Contrat:</strong> {{ contract }}</p>
    <p v-if="duration"><strong>Durée:</strong> {{ duration }}</p>
    <p v-if="date"><strong>Date de publication:</strong> {{ date }}</p>
    <br>
    <div id="row">
    <button><a :href="link" target="_blank" rel="noopener noreferrer">Voir l'offre</a></button>
    <select v-model="selectedTemplate">
      <option value="alternance">alternance</option>
      <option value="CDD">CDD</option>
      <option value="CDI">CDI</option>
    </select>
    <button @click="$emit('generateLetter', { company, title, template: selectedTemplate})"> générer </button>
  </div>
  </div>
</template>

<style scoped>
.card {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 16px;
  margin: 8px 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 30%;
  min-width: 250px;
  max-width: 350px;
  max-height: 350px;
  height: auto;
  min-height: 200px;

}
.card h3 {
  margin: 0 0 8px;
  font-size: 18px;
}
.card p {
  margin: 4px 0;
  font-size: 14px;
  text-overflow: ellipsis;
}
.card a {
  color: #ffffff;
  text-decoration: none;
}
.card a:hover {
  text-decoration: underline;
}

.card button {
  position: relative;
  bottom: 0;
  background-color: #007bff;
  color: white;
  border: none;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
}

.card button:last-child {
  background-color: #06d630;
}

#row{
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}
</style>