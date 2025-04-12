<script setup>
import { ref, onMounted } from 'vue'
import CardComponent from '../components/cardComponent.vue'

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
    <div v-for="(jobList, source) in jobs" :key="source">
      <h2>{{ source }}</h2>
      <div>
        <CardComponent
          v-for="job in jobList"
          :key="job"
          :title="job"
          :link="job"
        />
      </div>
    </div>
  </main>
</template>