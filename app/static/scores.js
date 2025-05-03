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
  const search_container = $("#search-results");
  const db_container = $("#db-results");
  
  // We don't want to empty the containers every time, this will be specified in the response
  emptyContainer(search_container);
  emptyContainer(db_container);

  renderContainer(search_container, response.search_results);
  renderContainer(db_container, response.db_results);
}

// Remove the currently loaded items
function emptyContainer(container) {

}

// Create the items and append the items to the container
function renderContainer(container, items) {
  for (let i in items) {
    const item = createItem(items[i]);
    container.appendChild(item);
  }
}

// Create an item from data
function createItem(item) {

}