<script setup>
import { ref, onMounted } from 'vue'

const jobs = ref([])

onMounted(async () => {
  try {
    const response = await fetch('http://localhost:8000/jobs') 
    const data = await response.json()
    jobs.value = data.jobs
    console.log('Jobs fetched successfully:', jobs.value)
  } catch (error) {
    console.error('Erreur lors de la récupération des jobs:', error)
  }
})
</script>

<template>
  <main>
    <h1>Liste des offres d'emploi</h1>
    <ul>
      <li v-for="(jobList, source) in jobs" :key="source">
        <h2>{{ source }}</h2>
        <ul>
          <li v-for="job in jobList" :key="job">{{ job }}</li>
        </ul>
      </li>
    </ul>
  </main>
</template>