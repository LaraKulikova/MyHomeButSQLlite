function openExpenseModal(expenseId) {
var modal = document.getElementById("deleteModal");
var form = document.getElementById("deleteForm");
form.action = "/delete_expense/" + expenseId + "/";
modal.style.display = "block";
}

function openIncomeModal(incomeId) {
var modal = document.getElementById("deleteModal");
var form = document.getElementById("deleteForm");
form.action = "/delete_income/" + incomeId + "/";
modal.style.display = "block";
}

function closeModal() {
var modal = document.getElementById("deleteModal");
modal.style.display = "none";
}

window.onclick = function(event) {
var modal = document.getElementById("deleteModal");
if (event.target === modal) {
modal.style.display = "none";
}
}