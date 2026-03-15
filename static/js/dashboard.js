const makeChart = (id, type, label, series) => {
  new Chart(document.getElementById(id), {
    type,
    data: {
      labels: series.map(s => s.label),
      datasets: [{ label, data: series.map(s => s.value), borderWidth: 2 }]
    },
    options: { responsive: true, animation: { duration: 900 } }
  });
};

async function loadCharts() {
  const res = await fetch('/api/analytics');
  const data = await res.json();
  makeChart('deptChart', 'bar', 'Complaints by Department', data.department);
  makeChart('priorityChart', 'pie', 'Priority Distribution', data.priority);
  makeChart('responseChart', 'line', 'Avg Response Time (hrs)', data.response_time);
  makeChart('trendChart', 'line', 'Complaint Trend', data.trend);
}

loadCharts();
