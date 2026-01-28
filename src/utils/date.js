export const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  const formatted = new Intl.DateTimeFormat('cs-CZ', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  }).format(date);

  // Capitalize first letter to match style like "Pátek 13. března 2026"
  return formatted.charAt(0).toUpperCase() + formatted.slice(1);
};

// Helper to parse YYYY-MM-DD as local date (midnight)
export const parseLocalDate = (dateStr) => {
  const [y, m, d] = dateStr.split('-').map(Number);
  return new Date(y, m - 1, d);
};


