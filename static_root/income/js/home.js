document.addEventListener('DOMContentLoaded', function () 
{
    const closeEditModeButton = document.querySelector('.close-edit-button');
    const selectAllContainer = document.getElementById('select-all-container');
    const selectAllCheckbox = document.getElementById('select-all');
    const checkboxes = document.querySelectorAll('.select-checkbox');

    closeEditModeButton.style.display = 'none';
    selectAllContainer.style.display = 'none';

    $(document).ready(function () {
      var table = $('#income-table').DataTable({
        searching: true,
        paging: true,
        ordering: true,
        order: [[0, 'asc']], // Replace 0 with the index of the column you want to initially order by
        columnDefs: [
          { orderable: false, targets: [2] } // Make the third column (index 2) not orderable
        ],
      });
        let firstRecordId = 0;
      var firstRecordId = $('#income-table tbody tr:first-child').data('income-id');
      console.log();
      document.write(firstRecordId.value);
      showDetails(firstRecordId);

      $('.select-checkbox').on('change', updateSelectedCount);
      $('#select-all').on('change', toggleAllCheckboxes);
  })});

function showDetails(incomeId) {
  const selectedRow = document.querySelector('.record-item[data-income-id="' + incomeId + '"]');

  if (selectedRow) {
    fetch(`/income/get-income-details/${incomeId}/`)
      .then(response => response.text())
      .then(data => {
        document.getElementById('details-view').innerHTML = data;
      });

    const allRows = document.querySelectorAll('.record-item');
    allRows.forEach(row => {
      row.classList.remove('selected');
    });
    selectedRow.classList.add('selected');
  }
}

function toggleAllCheckboxes() {
  const checkboxes = document.getElementsByName('selected_items');
  const selectAllCheckbox = document.getElementById('select-all');
  checkboxes.forEach((checkbox) => {
    checkbox.checked = selectAllCheckbox.checked;
  });

  updateSelectedCount();
}

function toggleEditMode() {
  const editModeButton = document.querySelector('.edit-button');
  const closeEditModeButton = document.querySelector('.close-edit-button');
  const massActionRow = document.querySelector('.records-list-container');
  const recordsListTable = document.querySelector('.records-list');

  const newColumn = document.querySelector('.checkbox-column');

  if (!newColumn) {
    const newTh = document.createElement('th');
    newTh.className = 'checkbox-column';

    const checkboxHeader = document.createElement('input');
    checkboxHeader.type = 'checkbox';
    checkboxHeader.id = 'select-all';
    checkboxHeader.onclick = toggleAllCheckboxes;

    newTh.appendChild(checkboxHeader);
    recordsListTable.querySelector('thead tr').prepend(newTh);

    recordsListTable.querySelectorAll('tbody tr').forEach((row) => {
      const newTd = document.createElement('td');
      newTd.className = 'checkbox-column';

      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.className = 'select-checkbox';
      checkbox.name = 'selected_items';
      checkbox.value = row.dataset.incomeId;

      newTd.appendChild(checkbox);
      row.prepend(newTd);
    });
  }

  massActionRow.classList.add('edit-mode');
  editModeButton.style.display = 'none';
  closeEditModeButton.style.display = 'inline-block';

  const checkboxes = document.querySelectorAll('.checkbox-column .select-checkbox');
  checkboxes.forEach((checkbox) => {
    checkbox.style.display = 'inline-block';
  });

  updateSelectedCount();
}

function closeEditMode() {
  const editModeButton = document.querySelector('.edit-button');
  const closeEditModeButton = document.querySelector('.close-edit-button');
  const massActionRow = document.querySelector('.records-list-container');
  const recordsListTable = document.querySelector('.records-list');

  const newColumn = document.querySelector('.checkbox-column');
  if (newColumn) {
    newColumn.remove();

    recordsListTable.querySelectorAll('tbody tr').forEach((row) => {
      const cell = row.querySelector('.checkbox-column');
      if (cell) {
        cell.remove();
      }
    });
  }

  massActionRow.classList.remove('edit-mode');
  editModeButton.style.display = 'inline-block';
  closeEditModeButton.style.display = 'none';

  const checkboxes = document.querySelectorAll('.checkbox-column .select-checkbox');
  checkboxes.forEach((checkbox) => {
    checkbox.style.display = 'none';
  });

  updateSelectedCount();
}

function updateSelectedCount() {
  const selectedCount = document.querySelectorAll('.checkbox-column .select-checkbox:checked').length;
  document.getElementById('selected-count').innerText = selectedCount;
}

function performMassAction() {
  const selectedItems = document.querySelectorAll('.checkbox-column .select-checkbox:checked');
  const selectedIds = Array.from(selectedItems).map(checkbox => checkbox.value);

  // Now you can perform the mass action with the selected IDs
  // For example, you can send an AJAX request to the mass-action URL
  // Replace 'YOUR_MASS_ACTION_URL' with your actual URL
  const massActionUrl = 'income/mass-action/';
  fetch(massActionUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken') // Ensure to include CSRF token
    },
    body: JSON.stringify({ selected_ids: selectedIds })
  })
  .then(response => {
    // Handle the response as needed
    console.log(response);
  });
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}