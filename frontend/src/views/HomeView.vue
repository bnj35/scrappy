<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import { useJobStore } from '../stores/jobStore'
import CardComponent from '../components/cardComponent.vue'

const jobStore = useJobStore()
const scrapingStatus = ref('idle')
let fetchInterval = null

// État pour suivre combien d'annonces afficher par source
const visibleCounts = ref({})

watch(
  () => jobStore.jobs,
  (newJobs) => {
    if (newJobs.length > 0) {
      initializeVisibleCounts()
    }
  },
  { immediate: true }
)

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
      console.log('Scraping completed:', data.jobs)
      jobStore.updateJobsDb(data.jobs);
      await jobStore.fetchJobs() 
      initializeVisibleCounts() 
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
      const response = await fetch('http://localhost:8000/jobs')
      const data = await response.json()
      jobStore.jobs = data.jobs
      console.log('No jobs found, starting scraping...')
      await startScraping()
    } else {
      initializeVisibleCounts() // Réinitialiser les comptes visibles après le fetch
    }
  } catch (error) {
    console.error('Error fetching jobs:', error)
  }
}

const handleGenerateLetter = (data) => {
  const { company, title, template } = data
  console.log(`Generating letter for ${company} regarding position: ${title} using template: ${template}`)
  
  let formatTitle = title.replace(/[^a-zA-Z0-9 ]/g, '').replace(/\s+/g, ' ')
  // Select template based on the template value
  let letterContent = ''
  
  if (template === 'alternance') {
    letterContent = `
AUGER Benjamin
18 rue Victor Lemoine
54000 Nancy
07 69 23 05 71
benjaminauger35@gmail.com
Portfolio :
https://bnj.vercel.app/
https://benjamin-auger-portfolio.vercel.app/

Objet : Candidature - ${formatTitle} - (alternance dans le cadre du Mastère Dev Manager Fullstack de l’EFREI Bordeaux)

Madame, Monsieur,

Actuellement en dernière année de BUT MMI, parcours Développement Web et Multimédia, je suis admis au Mastère Dev Manager Fullstack de l’EFREI Bordeaux pour la rentrée prochaine. 
Dans ce cadre, je suis à la recherche d’une entreprise pour une alternance me permettant de poursuivre ma montée en compétences tout en contribuant activement à des projets concrets.
Durant mes études, j’ai eu l’opportunité de développer un socle technique solide en développement web : HTML, CSS, JavaScript, Node.js, PHP, SQL, ainsi que des frameworks comme Next.js, Vue.js et Slim. Je me suis également initié au développement mobile avec Flutter et Dart. Ces compétences, je les ai mises en pratique à travers divers projets universitaires et professionnels, en particulier lors de stages en entreprise.

Parallèlement à mon parcours académique, mon activité de graphiste freelance m’a permis de renforcer mon autonomie, ma rigueur, et mon sens du design.Cette double compétence, technique et créative, me permet d’avoir une vision globale des projets, de la conception à la mise en production.

Intégrer ${company} en alternance serait pour moi l’occasion de continuer à progresser dans un environnement professionnel, tout en apportant mes connaissances, mon enthousiasme et ma curiosité. Je suis particulièrement motivé par les missions de développement web fullstack, l’optimisation des interfaces. De plus j'ai l'habitude du travail en équipe et l’utilisation d’outils collaboratifs comme GitHub, GitLab, Jira ou encore Figma.

Je vous remercie pour votre attention et reste à votre disposition pour toute information complémentaire.
Je vous prie d’agréer, Madame, Monsieur, l’expression de mes salutations distinguées.

Benjamin Auger
    `
  } else if (template === 'CDD') {
    letterContent = `
AUGER Benjamin
18 rue Victor Lemoine
54000 Nancy
07 69 23 05 71
benjaminauger35@gmail.com
Portfolio :
https://bnj.vercel.app/
https://benjamin-auger-portfolio.vercel.app/

Objet : Candidature - ${formatTitle}

Madame, Monsieur,

Actuellement en dernière année de BUT MMI, parcours Développement Web et Multimédia, je suis admis au Mastère Dev Manager Fullstack de l’EFREI Bordeaux pour la rentrée prochaine. 
Dans ce cadre, je suis à la recherche d’une entreprise pour une alternance me permettant de poursuivre ma montée en compétences tout en contribuant activement à des projets concrets.
Durant mes études, j’ai eu l’opportunité de développer un socle technique solide en développement web : HTML, CSS, JavaScript, Node.js, PHP, SQL, ainsi que des frameworks comme Next.js, Vue.js et Slim. Je me suis également initié au développement mobile avec Flutter et Dart. Ces compétences, je les ai mises en pratique à travers divers projets universitaires et professionnels, en particulier lors de stages en entreprise.

Parallèlement à mon parcours académique, mon activité de graphiste freelance m’a permis de renforcer mon autonomie, ma rigueur, et mon sens du design.Cette double compétence, technique et créative, me permet d’avoir une vision globale des projets, de la conception à la mise en production.

Intégrer ${company} en alternance serait pour moi l’occasion de continuer à progresser dans un environnement professionnel, tout en apportant mes connaissances, mon enthousiasme et ma curiosité. Je précise que ma candidature concerne uniquement une alternance dans le cadre de ma formation, et non un contrat à durée déterminée (${template}) comme indiqué dans l’annonce. Je suis particulièrement motivé par les missions de développement web fullstack, l’optimisation des interfaces. De plus j'ai l'habitude du travail en équipe et l’utilisation d’outils collaboratifs comme GitHub, GitLab, Jira ou encore Figma.

Je vous remercie pour votre attention et reste à votre disposition pour toute information complémentaire.
Je vous prie d’agréer, Madame, Monsieur, l’expression de mes salutations distinguées.

Benjamin Auger
    `
  }
  else if (template === 'CDI') {
    letterContent = `
AUGER Benjamin
18 rue Victor Lemoine
54000 Nancy
07 69 23 05 71
benjaminauger35@gmail.com
Portfolio :
https://bnj.vercel.app/
https://benjamin-auger-portfolio.vercel.app/

Objet : Candidature - ${formatTitle}

Madame, Monsieur,

Actuellement en dernière année de BUT MMI, parcours Développement Web et Multimédia, je suis admis au Mastère Dev Manager Fullstack de l’EFREI Bordeaux pour la rentrée prochaine. 
Dans ce cadre, je suis à la recherche d’une entreprise pour une alternance me permettant de poursuivre ma montée en compétences tout en contribuant activement à des projets concrets.
Durant mes études, j’ai eu l’opportunité de développer un socle technique solide en développement web : HTML, CSS, JavaScript, Node.js, PHP, SQL, ainsi que des frameworks comme Next.js, Vue.js et Slim. Je me suis également initié au développement mobile avec Flutter et Dart. Ces compétences, je les ai mises en pratique à travers divers projets universitaires et professionnels, en particulier lors de stages en entreprise.

Parallèlement à mon parcours académique, mon activité de graphiste freelance m’a permis de renforcer mon autonomie, ma rigueur, et mon sens du design.Cette double compétence, technique et créative, me permet d’avoir une vision globale des projets, de la conception à la mise en production.

Intégrer ${company} en alternance serait pour moi l’occasion de continuer à progresser dans un environnement professionnel, tout en apportant mes connaissances, mon enthousiasme et ma curiosité. Je précise que ma candidature concerne uniquement une alternance dans le cadre de ma formation, et non un contrat à durée indétermninée (${template}) comme indiqué dans l’annonce. Je suis particulièrement motivé par les missions de développement web fullstack, l’optimisation des interfaces. De plus j'ai l'habitude du travail en équipe et l’utilisation d’outils collaboratifs comme GitHub, GitLab, Jira ou encore Figma.

Je vous remercie pour votre attention et reste à votre disposition pour toute information complémentaire.
Je vous prie d’agréer, Madame, Monsieur, l’expression de mes salutations distinguées.

Benjamin Auger
    `
  }
  // Create a temporary element to generate the PDF
  const element = document.createElement('div')
  element.innerHTML = `
    <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 20px auto; padding: 20px; white-space: pre-wrap; text-align: justify;">
      ${letterContent}
    </div>
  `
  document.body.appendChild(element)
  
  // Use html2pdf library to generate PDF
  import('html2pdf.js').then((html2pdf) => {
    const options = {
      margin: 1,
      filename: `lettre_motivation_${company.replace(/\s+/g, '_')}.pdf`,
      image: { type: 'jpeg', quality: 0.98 },
      html2canvas: { scale: 2 },
      jsPDF: { unit: 'cm', format: 'a4', orientation: 'portrait' },
    }
    
    html2pdf.default(element, options).then(() => {
      // Remove the temporary element after PDF generation
      document.body.removeChild(element)
    })
  }).catch(error => {
    console.error('Error generating PDF:', error)
    alert('Erreur lors de la génération du PDF. Veuillez réessayer.')
    document.body.removeChild(element)
  })
  
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
      <button @click="jobStore.clearJobs">
        Effacer les offres
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
              :date="job.date" :duration="job.duration" :link="job.offer_url" @generateLetter="handleGenerateLetter" />
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