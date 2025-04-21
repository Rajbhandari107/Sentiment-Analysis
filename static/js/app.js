// Theme toggle functionality
const themeToggle = document.getElementById('themeToggle');
const body = document.body;

// Check for saved theme preference or use preferred color scheme
const currentTheme = localStorage.getItem('theme') || 
                    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');

// Apply the current theme
if (currentTheme === 'dark') {
  body.classList.add('dark-mode');
  themeToggle.textContent = 'Light Mode';
}

// Theme toggle button event
themeToggle.addEventListener('click', () => {
  body.classList.toggle('dark-mode');
  const isDark = body.classList.contains('dark-mode');
  themeToggle.textContent = isDark ? 'Light Mode' : 'Dark Mode';
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
});

// Sample tweets button functionality
document.getElementById('sampleBtn')?.addEventListener('click', () => {
  const sampleTweets = [
    "Just had an amazing day at the beach! 🌊☀️ #summer",
    "Traffic is terrible this morning. Wasting so much time...",
    "The new movie was okay, not great but not bad either",
    "@Tesla The new update is fantastic! Loving the improvements",
    "Why does everything have to be so complicated? Ugh"
  ].join('\n');

  document.querySelector('textarea[name="tweets"]').value = sampleTweets;
});
