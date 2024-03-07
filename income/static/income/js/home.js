document.addEventListener('DOMContentLoaded', function () {
  // Hide the "Close Edit" button initially
  const closeEditModeButton = document.querySelector('.close-edit-button');
  closeEditModeButton.style.display = 'none';

  var table = $('.records-list').DataTable({
      searching: true,
      paging: true,
      ordering: true,
      order: [[1, 'asc']],  // Initial order by the second column (Day)
  });

  // Get the ID of the first record
  var firstRecordId = $('.records-list tbody tr:first-child').data('income-id');
  // Call showDetails with the ID of the first record
  showDetails(firstRecordId);

  // Add event listener to each checkbox to capture selected IDs and pass to delete button
  const recordsListTable = document.querySelector('.records-list');  // Add this line
  recordsListTable.querySelectorAll('.select-checkbox').forEach((checkbox) => {
      checkbox.addEventListener('change', (event) => {
          const selectedIds = getSelectedIncomeIds();
          passSelectedIdsToDeleteButton(selectedIds);
      });
  });
});

function showDetails(incomeId) {
    const selectedRow = document.querySelector('.record-item[data-income-id="' + incomeId + '"]');

    if (selectedRow) {
        fetch('/income/get-income-details/' + incomeId + '/')
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

let selectedIds = []; // Initialize empty array

function toggleEditMode() {
    const editModeButton = document.querySelector('.edit-button');
    const closeEditModeButton = document.querySelector('.close-edit-button');
    const massActionRow = document.querySelector('.records-list-container');
    const recordsListTable = document.querySelector('.records-list');

    // Check if the new column already exists
    const newColumn = document.querySelector('.checkbox-column');

    if (!newColumn) {
        // Create a new column for checkboxes
        const newTh = document.createElement('th');
        newTh.className = 'checkbox-column';

        // Create a checkbox for the header
        const checkboxHeader = document.createElement('input');
        checkboxHeader.type = 'checkbox';
        checkboxHeader.id = 'select-all';
        checkboxHeader.onclick = toggleAllCheckboxes;

        newTh.appendChild(checkboxHeader);
        recordsListTable.querySelector('thead tr').prepend(newTh);

        // Loop through each row to add a new cell in the new column for checkboxes
        recordsListTable.querySelectorAll('tbody tr').forEach((row) => {
            const newTd = document.createElement('td');
            newTd.className = 'checkbox-column';

            // Create a checkbox for each row
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

    // Remove the new column for checkboxes
    const newColumn = document.querySelector('.checkbox-column');
    if (newColumn) {
        newColumn.remove();

        // Loop through each row to remove the cell in the new column for checkboxes
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

function toggleAllCheckboxes() {
    const checkboxes = document.getElementsByName('selected_items');
    const selectAllCheckbox = document.getElementById('select-all');
    checkboxes.forEach((checkbox) => {
        checkbox.checked = selectAllCheckbox.checked;
    });

    updateSelectedCount();
}

function passSelectedIdsToDeleteButton(selectedIds) {
    // Assuming you have a delete button with the id 'delete-selected-button'
    const deleteButton = document.getElementById('delete-selected-button');
    
    // Attach the selectedIds to the button (for example, using a custom attribute)
    deleteButton.setAttribute('data-selected-ids', JSON.stringify(selectedIds));
}

function performMassAction() {
    const selectedItems = document.querySelectorAll('.checkbox-column .select-checkbox:checked');
    const selectedIds = Array.from(selectedItems).map(checkbox => checkbox.value);

    // Now you can perform the mass action with the selected IDs
    // For example, you can send an AJAX request to the mass-action URL
    // Replace 'YOUR_MASS_ACTION_URL' with your actual URL
    const massActionUrl = '/income/mass-action/';
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

// Function to get CSRF token from cookies
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
