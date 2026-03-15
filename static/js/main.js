const toast = (msg) => {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.remove('hidden');
  setTimeout(() => el.classList.add('hidden'), 2500);
};

const withLoading = async (button, action) => {
  const old = button.textContent;
  button.textContent = 'Loading...';
  button.disabled = true;
  try { await action(); } finally { button.textContent = old; button.disabled = false; }
};

document.getElementById('submitComplaint').addEventListener('click', async (e) => {
  const text = document.getElementById('complaintText').value.trim();
  if (!text) return toast('Please enter complaint text');

  await withLoading(e.target, async () => {
    const res = await fetch('/api/complaints', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text })
    });
    const data = await res.json();
    document.getElementById('complaintResult').innerHTML =
      `<b>ID:</b> ${data.id} | <b>Department:</b> ${data.department} | <b>Priority:</b> ${data.priority}`;
    toast('Complaint submitted successfully');
  });
});

document.getElementById('submitQuery').addEventListener('click', async (e) => {
  const question = document.getElementById('queryText').value.trim();
  if (!question) return toast('Please enter a question');

  await withLoading(e.target, async () => {
    const res = await fetch('/api/query', {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ question })
    });
    const data = await res.json();
    document.getElementById('queryResult').innerHTML =
      `<b>Answer:</b> ${data.answer}<br><b>Department:</b> ${data.department}<br><b>Similarity:</b> ${Number(data.score).toFixed(3)}`;
    toast('Query processed');
  });
});
