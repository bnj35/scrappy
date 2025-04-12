<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import { useJobStore } from '../stores/jobStore'
import CardComponent from '../components/cardComponent.vue'

const jobStore = useJobStore()
const scrapingStatus = ref('idle')
let fetchInterval = null

// État pour suivre combien d'annonces afficher par source
const visibleCounts = ref({})

// Fonction pour augmenter le nombre d'annonces visibles pour une source
const showMore = (source) => {
  if (!visibleCounts.value[source]) {
    visibleCounts.value[source] = 8
  }
  visibleCounts.value[source] += 8
}

// Initialiser les comptes visibles pour chaque source
const initializeVisibleCounts = () => {
  Object.keys(jobsBySource.value).forEach((source) => {
    if (!visibleCounts.value[source]) {
      visibleCounts.value[source] = 8
    }
  })
}

// Computed property pour regrouper les jobs par source
const jobsBySource = computed(() => {
  return jobStore.jobs.reduce((acc, job) => {
    if (!acc[job.source]) {
      acc[job.source] = []
    }
    acc[job.source].push(job)
    return acc
  }, {})
})

// Fonction pour vérifier le statut du scraping
const checkScrapingStatus = async () => {
  try {
    const response = await fetch('http://localhost:8000/scrap-jobs')
    const data = await response.json()
    scrapingStatus.value = data.status

    if (data.status === 'completed') {
      await jobStore.fetchJobs()
      initializeVisibleCounts() // Réinitialiser les comptes visibles après le fetch
      console.log('Jobs fetched successfully:', jobStore.jobs)
    }
  } catch (error) {
    console.error('Error checking scraping status:', error)
  }
}

// Fonction pour démarrer le scraping
const startScraping = async () => {
  try {
    scrapingStatus.value = 'started'
    const response = await fetch('http://localhost:8000/start-scraping', {
      method: 'POST',
    })
    const data = await response.json()
    scrapingStatus.value = data.status
    console.log('Scraping started:', data)
  } catch (error) {
    scrapingStatus.value = 'error'
    console.error('Error starting scraping:', error)
  }
}

// Fonction pour récupérer les jobs
const fetchJobs = async () => {
  try {
    await jobStore.fetchJobs()
    if (jobStore.jobs.length === 0) {
      console.log('No jobs found, starting scraping...')
      await startScraping()
    } else {
      initializeVisibleCounts() // Réinitialiser les comptes visibles après le fetch
    }
  } catch (error) {
    console.error('Error fetching jobs:', error)
  }
}

onMounted(() => {
  fetchJobs()

  fetchInterval = setInterval(() => {
    if (scrapingStatus.value === 'started' || scrapingStatus.value === 'in_progress') {
      console.log('Checking scraping status...')
      checkScrapingStatus()
    }
  }, 5000)
})

onUnmounted(() => {
  if (fetchInterval) {
    clearInterval(fetchInterval)
  }
})
</script>

<template>
  <main>
    <h1>Liste des offres d'emploi</h1>
    <div class="buttons">
      <button @click="startScraping">
        Chercher des offres d'emploi
      </button>
      <button @click="fetchJobs">
        Rafraîchir
      </button>
    </div>

    <div v-if="scrapingStatus === 'error'">
      <p>Une erreur s'est produite lors du scraping. Veuillez réessayer.</p>
      <button @click="startScraping">Réessayer</button>
    </div>
    <div v-if="scrapingStatus === 'started'">
      <p>Le scraping a commencé.</p>
    </div>
    <div v-if="scrapingStatus === 'in_progress' || scrapingStatus === 'already_in_progress'">
      <p>Scraping en cours... Veuillez patienter.</p>
    </div>
    <div v-if="scrapingStatus === 'completed' || Object.keys(jobsBySource).length > 0">
      <div v-for="(jobList, source) in jobsBySource" :key="source">
        <div v-if="jobList.length > 0" class="job-list">
          <h2>{{ source }}</h2>
          <div class="card-grid">
            <CardComponent v-for="(job, index) in jobList.slice(0, visibleCounts[source] || 9)" :key="job.offer_url"
              :title="job.title" :company="job.company" :location="job.location" :contract="job.contract"
              :date="job.date" :duration="job.duration" :link="job.offer_url" />
          </div>
          <button v-if="visibleCounts[source] < jobList.length" @click="showMore(source)">
            Afficher plus
          </button>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.card-grid {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 16px;
}

h2 {
  margin-block: 2rem;
  font-size: 100px;
  font-weight: bold;
}

main {
  padding: 2em;
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

button {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.job-list {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.buttons {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}
</style>