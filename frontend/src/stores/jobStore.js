import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useJobStore = defineStore('jobStore', () => {
  const jobs = ref([])


  const fetchJobs = async () => {
    try {
      console.log('Fetching jobs...')
      const response = await fetch('http://localhost:8000/jobs')
      const data = await response.json()
      jobs.value = data.jobs
      console.log('Jobs fetched:', jobs.value)
    } catch (error) {
      console.error('Error fetching jobs:', error)
    }
  }

  const updateJobsDb = async (jobData) => {
    try {
      // Flatten the job data into a single list
      const formattedJobs = Object.entries(jobData).flatMap(([source, jobs]) =>
        jobs.map((job) => ({
          source, // Add the source (e.g., "hellowork", "wttj") to each job
          title: job.title,
          company: job.company || null,
          location: job.location || null,
          contract: job.contract || null,
          duration: job.duration || null,
          date: job.date || null,
          offer_url: job.offer_url,
        }))
      );
  
      console.log('Sending job data to backend:', formattedJobs); // Log the formatted data
  
      const response = await fetch('http://localhost:8000/jobs', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formattedJobs), // Send the flattened list
      });
  
      if (!response.ok) {
        throw new Error('Failed to update jobs in the database');
      }
  
      await fetchJobs();
    } catch (error) {
      console.error('Error updating jobs:', error);
    }
  };

  const startScraping = async () => {
    try {
      const response = await fetch('http://localhost:8000/start-scraping', {
        method: 'POST',
      })
      const data = await response.json()
      console.log('Scraping started:', data)
    } catch (error) {
      console.error('Error starting scraping:', error)
    }
  }
  return {
    jobs,
    fetchJobs,
    updateJobsDb,
    startScraping,
  }
})