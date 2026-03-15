async function loadComplaints() {
  const filter = document.getElementById('departmentFilter').value.trim();
  const url = filter ? `/api/complaints?department=${encodeURIComponent(filter)}` : '/api/complaints';
  const res = await fetch(url);
  const data = await res.json();

  const table = document.getElementById('complaintsTable');
  table.innerHTML = '';
  for (const c of data) {
    const badge = c.priority === 'HIGH' ? 'bg-red-100 text-red-700' : c.priority === 'LOW' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700';
    const tr = document.createElement('tr');
    tr.className = 'border-b';
    tr.innerHTML = `
      <td class="p-2">${c.id}</td>
      <td class="p-2 max-w-sm">${c.complaint_text}</td>
      <td class="p-2">${c.department}</td>
      <td class="p-2"><span class="px-2 py-1 rounded ${badge}">${c.priority}</span></td>
      <td class="p-2">${c.status}</td>
      <td class="p-2">
        <button class="bg-emerald-600 text-white px-2 py-1 rounded" onclick="resolveComplaint(${c.id})">Resolve</button>
      </td>`;
    table.appendChild(tr);
  }
}

async function resolveComplaint(id) {
  const resolution = prompt('Enter resolution text');
  if (!resolution) return;
  await fetch(`/api/complaints/${id}/resolve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ resolution })
  });
  loadComplaints();
}

document.getElementById('loadComplaints').addEventListener('click', loadComplaints);
loadComplaints();
