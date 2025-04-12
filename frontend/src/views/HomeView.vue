<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useJobStore } from '../stores/jobStore'
import CardComponent from '../components/cardComponent.vue'

const jobStore = useJobStore()
const scrapingStatus = ref('idle') // Indique l'état du scraping
let fetchInterval = null

const checkScrapingStatus = async () => {
  try {
    const response = await fetch('http://localhost:8000/jobs')
    const data = await response.json()
    scrapingStatus.value = data.status

    if (data.status === 'completed') {
      jobStore.jobs = data.jobs
      console.log('Jobs fetched successfully:', jobStore.jobs)
    }
  } catch (error) {
    console.error('Error checking scraping status:', error)
  }
}

const startScraping = async () => {
  try {
    const response = await fetch('http://localhost:8000/start-scraping', {
      method: 'POST',
    })
    const data = await response.json()
    scrapingStatus.value = data.status
    console.log('Scraping started:', data)
  } catch (error) {
    console.error('Error starting scraping:', error)
  }
}

onMounted(() => {
  // Démarre le scraping
  startScraping()

  fetchInterval = setInterval(() => {
    console.log('Checking scraping status...')
    checkScrapingStatus()
  }, 5000)
})

onUnmounted(() => {
  // Nettoie l'intervalle lorsque le composant est démonté
  if (fetchInterval) {
    clearInterval(fetchInterval)
  }
})
</script>

<template>
  <main>
    <h1>Liste des offres d'emploi</h1>
    <div v-if="scrapingStatus === 'idle'">
      <p>Aucune tâche de scraping en cours.</p>
      <button @click="startScraping">Démarrer le scraping</button>
    </div>
    <div v-if="scrapingStatus === 'error'">
      <p>Une erreur s'est produite lors du scraping. Veuillez réessayer.</p>
      <button @click="startScraping">Réessayer</button>
    </div>
    <div v-if="scrapingStatus === 'started'">
      <p>le Scraping a commencé.</p>
    </div>
    <div v-if="scrapingStatus === 'in_progress' || scrapingStatus === 'already_in_progress'" >
      <p>Scraping en cours... Veuillez patienter.</p>
    </div>
    <div v-if="scrapingStatus === 'completed'">
      <p>Scraping terminé !</p>
      <div v-for="(jobList, source) in jobStore.jobs" :key="source">
        <div v-if="jobList.length > 0">
          <h2>{{ source }}</h2>
          <div class="card-grid">
            <CardComponent
              v-for="job in jobList"
              :key="job.offer_url"
              :title="job.title"
              :company="job.company"
              :location="job.location"
              :contract="job.contract"
              :date="job.date"
              :duration="job.duration"
              :link="job.offer_url"
            />
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.card-grid {
  width: 100%;
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 3 colonnes */
  gap: 16px; /* Espacement entre les cartes */
}

h2 {
  margin-block: 2rem;
  font-size: 100px;
  font-weight: bold;
}

main {
  padding: 2em;
  background-color: #f9f9f9;
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>