const chartTheme = {
  color: '#e2e8f0',
  borderColor: 'rgba(148, 163, 184, 0.2)'
};

const createChart = (id, type, label, series, color) => {
  new Chart(document.getElementById(id), {
    type,
    data: {
      labels: series.map((point) => point.label),
      datasets: [{
        label,
        data: series.map((point) => point.value),
        borderWidth: 2,
        borderColor: color,
        backgroundColor: `${color}66`,
        fill: type === 'line'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: { labels: { color: chartTheme.color } }
      },
      scales: {
        x: { ticks: { color: chartTheme.color }, grid: { color: chartTheme.borderColor } },
        y: { ticks: { color: chartTheme.color }, grid: { color: chartTheme.borderColor } }
      }
    }
  });
};

async function loadCharts() {
  const res = await fetch('/api/analytics');
  const data = await res.json();

  createChart('deptChart', 'bar', 'Complaints by Department', data.department, '#38bdf8');
  createChart('priorityChart', 'doughnut', 'Priority Distribution', data.priority, '#f472b6');
  createChart('responseChart', 'line', 'Average Response Time (hours)', data.response_time, '#a78bfa');
  createChart('trendChart', 'line', 'Complaint Trend', data.trend, '#4ade80');
}

loadCharts();
