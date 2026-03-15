const toast = (message, type = 'success') => {
  const el = document.getElementById('toast');
  el.textContent = message;
  el.className = `fixed right-4 bottom-4 rounded-lg px-4 py-3 shadow-lg text-white ${type === 'error' ? 'bg-rose-600' : 'bg-emerald-600'}`;
  el.classList.remove('hidden');
  setTimeout(() => el.classList.add('hidden'), 2600);
};

const toggleLoading = (id, show) => {
  const el = document.getElementById(id);
  if (!el) return;
  el.classList.toggle('hidden', !show);
};

const submitComplaint = async () => {
  const text = document.getElementById('complaintText').value.trim();
  const result = document.getElementById('complaintResult');
  if (!text) {
    toast('Please write a complaint first.', 'error');
    return;
  }

  toggleLoading('complaintLoader', true);
  result.classList.add('hidden');

  try {
    const response = await fetch('/api/complaints', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Failed to submit complaint.');

    result.innerHTML = `
      <h3 class="font-semibold text-base mb-2">AI Routing Result</h3>
      <p><strong>Department:</strong> ${data.department}</p>
      <p><strong>Priority:</strong> ${data.priority}</p>
      <p><strong>Sentiment:</strong> ${data.sentiment.label}</p>
    `;
    result.classList.remove('hidden');
    toast('Complaint submitted successfully.');
  } catch (error) {
    toast(error.message, 'error');
  } finally {
    toggleLoading('complaintLoader', false);
  }
};

const submitQuery = async () => {
  const question = document.getElementById('queryText').value.trim();
  const result = document.getElementById('queryResult');
  if (!question) {
    toast('Please type a question first.', 'error');
    return;
  }

  toggleLoading('queryLoader', true);
  result.classList.add('hidden');

  try {
    const response = await fetch('/api/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Failed to process query.');

    result.innerHTML = `
      <h3 class="font-semibold text-base mb-2">AI Answer</h3>
      <p><strong>Answer:</strong> ${data.answer}</p>
      <p><strong>Department:</strong> ${data.department}</p>
      <p><strong>Similarity:</strong> ${Number(data.score || 0).toFixed(3)}</p>
    `;
    result.classList.remove('hidden');
    toast('Answer generated.');
  } catch (error) {
    toast(error.message, 'error');
  } finally {
    toggleLoading('queryLoader', false);
  }
};

document.getElementById('submitComplaint').addEventListener('click', submitComplaint);
document.getElementById('submitQuery').addEventListener('click', submitQuery);
