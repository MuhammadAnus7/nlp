const adminToast = (message, error = false) => {
  const el = document.getElementById('adminToast');
  el.textContent = message;
  el.className = `fixed right-4 bottom-4 rounded-lg px-4 py-3 shadow-lg text-white ${error ? 'bg-rose-600' : 'bg-indigo-600'}`;
  el.classList.remove('hidden');
  setTimeout(() => el.classList.add('hidden'), 2400);
};

const priorityBadge = (priority) => {
  if (priority === 'HIGH') return 'bg-red-500/20 text-red-200 border-red-400/30';
  if (priority === 'LOW') return 'bg-emerald-500/20 text-emerald-200 border-emerald-400/30';
  return 'bg-amber-500/20 text-amber-200 border-amber-400/30';
};

async function loadComplaints() {
  const filter = document.getElementById('departmentFilter').value.trim();
  const url = filter ? `/api/complaints?department=${encodeURIComponent(filter)}` : '/api/complaints';
  const res = await fetch(url);
  const complaints = await res.json();

  const tbody = document.getElementById('complaintsTable');
  tbody.innerHTML = '';

  if (!complaints.length) {
    tbody.innerHTML = `<tr><td colspan="7" class="p-4 text-center text-slate-300">No complaints found.</td></tr>`;
    return;
  }

  complaints.forEach((item) => {
    const tr = document.createElement('tr');
    tr.className = 'border-t border-white/10 hover:bg-white/5 transition';
    tr.innerHTML = `
      <td class="p-3">${item.id}</td>
      <td class="p-3 max-w-md">${item.complaint_text}</td>
      <td class="p-3">${item.department}</td>
      <td class="p-3"><span class="px-2 py-1 text-xs rounded-full border ${priorityBadge(item.priority)}">${item.priority}</span></td>
      <td class="p-3">${item.sentiment_label || '-'}</td>
      <td class="p-3">${item.status}</td>
      <td class="p-3">
        <button class="px-3 py-1 rounded-lg bg-indigo-600 hover:bg-indigo-500 ${item.status === 'RESOLVED' ? 'opacity-50 cursor-not-allowed' : ''}" ${item.status === 'RESOLVED' ? 'disabled' : ''} onclick="resolveComplaint(${item.id})">Resolve</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

async function resolveComplaint(id) {
  const resolution = prompt('Enter resolution details');
  if (!resolution) return;

  const response = await fetch(`/api/complaints/${id}/resolve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ resolution })
  });
  const data = await response.json();
  if (!response.ok) {
    adminToast(data.error || 'Failed to resolve complaint.', true);
    return;
  }
  adminToast('Complaint resolved and queued for retraining.');
  loadComplaints();
}

document.getElementById('loadComplaints').addEventListener('click', loadComplaints);
loadComplaints();
