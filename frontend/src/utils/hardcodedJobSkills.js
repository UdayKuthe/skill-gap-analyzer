// Provide hardcoded skills for specific professions here.
// Fill the arrays with the exact skill names you want to use.

export const HARDCODED_JOB_SKILLS = {
  "Web Developers": ["HTML", "CSS", "JavaScript", "React", "Node.js", "Git", "RESTful APIs", "Database Management", "Responsive Design", "Testing/Debugging", "Package Managers (npm/yarn)", "Build Tools (Webpack/Vite)"],
  "Data Scientists": ["Python", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "SQL", "Statistical Analysis", "Data Visualization", "Machine Learning", "Jupyter Notebooks", "Big Data Tools", "Cloud Platforms (AWS/Azure/GCP)"]

};

export function getHardcodedSkillsForJob(jobName) {
  if (!jobName) return [];
  const normalize = (s) => String(s).trim().toLowerCase().replace(/\s+/g, ' ');
  const name = normalize(jobName);
  const singular = name.endsWith('s') ? name.slice(0, -1) : name;
  const plural = name.endsWith('s') ? name : name + 's';

  // Try exact, singular, plural against defined keys (normalized)
  for (const [key, value] of Object.entries(HARDCODED_JOB_SKILLS)) {
    const k = normalize(key);
    if (k === name || k === singular || k === plural) return value;
  }
  return [];
}


