document.addEventListener('DOMContentLoaded', function() {
  try {
    const summaryEl = document.getElementById('sentimentSummary');
    if (!summaryEl) {
      console.error('Sentiment summary element not found');
      showChartFallback();
      return;
    }
    
    const sentimentData = {
      positive: parseInt(summaryEl.dataset.positive),
      neutral: parseInt(summaryEl.dataset.neutral),
      negative: parseInt(summaryEl.dataset.negative)
    };

    if (isNaN(sentimentData.positive) || isNaN(sentimentData.neutral) || isNaN(sentimentData.negative)) {
      console.error('Invalid sentiment data values');
      showChartFallback();
      return;
    }

    const total = sentimentData.positive + sentimentData.neutral + sentimentData.negative;
    if (total <= 0) {
      console.warn('No sentiment data available');
      showChartFallback();
      return;
    }

    renderSentimentChart(sentimentData);
  } catch (error) {
    console.error('Error initializing sentiment chart:', error);
    showChartFallback();
  }
});

function showChartFallback() {
  const fallback = document.querySelector('.chart-fallback');
  if (fallback) fallback.style.display = 'block';
}

function renderSentimentChart(data) {
  const ctx = document.getElementById('sentimentChart').getContext('2d');
  
  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Positive', 'Neutral', 'Negative'],
      datasets: [{
        data: [data.positive, data.neutral, data.negative],
        backgroundColor: [
          '#4cc9f0',
          '#ffc107',
          '#f72585'
        ],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '70%',
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            usePointStyle: true,
            padding: 20,
            font: {
              family: 'Inter',
              size: 14
            }
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const total = context.dataset.data.reduce((a, b) => a + b, 0);
              const value = context.raw;
              const percentage = Math.round((value / total) * 100);
              return `${context.label}: ${value} (${percentage}%)`;
            }
          }
        }
      }
    }
  });
}
