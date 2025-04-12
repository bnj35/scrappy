import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useJobStore = defineStore('jobStore', () => {
  const jobs = ref({})
  const previousJobs = ref({})

  // Fetch jobs from the backend
  const fetchJobs = async () => {
    try {
      const response = await fetch('http://localhost:8000/jobs')
      const data = await response.json()

      // Store the current jobs in `previousJobs` before updating
      previousJobs.value = { ...jobs.value }
      jobs.value = data.jobs
      console.log('Jobs updated successfully:', jobs.value)
    } catch (error) {
      console.error('Error fetching jobs:', error)
    }
  }

  return {
    jobs,
    previousJobs,
    fetchJobs,
  }
})