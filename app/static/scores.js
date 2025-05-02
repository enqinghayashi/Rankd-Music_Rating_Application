/*
This causes the event to be triggered twice even though stopPropagation should fix that

$(document).ready(function() {
  $("#search-bar-input").on("keydown", function(e) {
    if (e.key == "Enter") getItems();
    e.stopPropagation();
  });
});
*/

// Handler is added in HTML on search bar
function handleKeyDown(e) {
  if (e.key == "Enter") getItems();
}

// Return the id of the selected radio button
function getRadioSelected(radios) {
  for (let i in radios) {
    const radio = radios[i];
    if (radio.checked) return radio.id;
  }
}

// Get the contents of the search bar and search options
function getSearchParameters() {
  const search = document.getElementById("search-bar-input").value; // using jquery breaks this
  const type = getRadioSelected(document.getElementsByName("filter"));
  const saved = document.getElementById("saved").checked; // using jquery breaks this too
  return {
    "search": search,
    "type": type,
    "saved": saved
  };
}

// Make a request to the server for the items
function getItems() {
  const params = getSearchParameters();
  $.ajax({
    url: "",
    type: "get",
    contentType: "application/json",
    data: params,
    success: function(response) {
      renderItems(response)
    }
  })
}

// Render the items on the page
function renderItems(response) {
  console.log(response)
}

// Remove the currently loaded items
function clearScores() {

}

// Create an item from data
function createItem() {

}