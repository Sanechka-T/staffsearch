const checkbox = document.getElementById('now');
const endDateField = document.getElementById('end_date');

checkbox.addEventListener('change', function() {
     endDateField.disabled = this.checked;
});