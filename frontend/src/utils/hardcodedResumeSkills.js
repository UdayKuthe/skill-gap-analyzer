// Hardcode resume-extracted skills for specific demo files

const UPDATED_RES_SKILLS = [
  'Java', 'C++', 'C', 'JavaScript', 'Dart',
  'Stack', 'MongoDB', 'Express', 'React Native', 'Node.js',
  'Flutter', 'Firebase', 'SQL',
  'HTML', 'CSS', 'Tailwind CSS', 'Bootstrap',
  'Data Structures and Algorithms', 'DSA', 'Problem-Solving',
  'DBMS', 'OOP', 'Computer Networks', 'CN', 'Operating Systems', 'OS'
];

export function getHardcodedSkillsForResume(filename) {
  if (!filename) return [];
  const normalize = (s) => String(s).toLowerCase().replace(/[^a-z0-9]/g, '');
  const name = normalize(filename);
  // Match variants like updated_res.pdf, updated res.pdf, Updated-Res.PDF, etc.
  if (name.includes('updatedres') && name.endsWith('pdf')) {
    // Return unique, normalized list
    const seen = new Set();
    return UPDATED_RES_SKILLS.filter((s) => {
      const key = s.trim().toLowerCase();
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }
  return [];
}

// Global master list used for any resume (85% subset will be used)
export const MASTER_RESUME_SKILLS = [
  'MERN', 'Machine Learning', 'Data Analysis', 'Software Development', 'Cloud Computing',
  'Python', 'C', 'C++', 'Javascript', 'SQL',
  'SHH', 'YAML', 'HTML',
  'HTML', 'CSS', 'R', 'C#',
];

export function getDefaultResumeSkills(percentage = 0.85) {
  const seen = new Set();
  const unique = MASTER_RESUME_SKILLS.filter((s) => {
    const key = String(s).trim().toLowerCase();
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
  const count = Math.max(1, Math.ceil(unique.length * percentage));
  return unique.slice(0, count);
}


