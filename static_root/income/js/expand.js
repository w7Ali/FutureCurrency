document.addEventListener('DOMContentLoaded', function () {
    const recurringForm = document.getElementById('recurring_form');
    const recurringTypeCheckbox = document.getElementById('id_recurring_type');

    if (recurringTypeCheckbox && recurringForm) {
        // Initially hide the recurring form if the checkbox is unchecked
        recurringForm.style.display = recurringTypeCheckbox.checked ? 'block' : 'none';

        recurringTypeCheckbox.addEventListener('change', function () {
            // Toggle the display style of recurring form based on checkbox state
            recurringForm.style.display = recurringTypeCheckbox.checked ? 'block' : 'none';
        });
    }
});
