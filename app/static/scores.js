import { renderContainer } from "./items.js";
import { getSearchParameters } from "./search.js";

$(document).ready(function() {
  $("#search-bar-input").on("keydown", function(e) {
    if (e.key == "Enter") getItems();
    e.stopPropagation();
  });
  
  $(".filter").click(function() {
    window.setTimeout(getItems, 10); // Timeout for 10ms before calling to give time for options to update
  });

  getItems();
});

// Make a request to the server for items
function getItems() {
  $("#search-results").empty();
  $("#db-results").empty();
  $("#placeholders").show();
  const params = getSearchParameters();
  requestItems(params);
}

// Make a request to the server for the items
function requestItems(params) {
  $.ajax({
    url: "",
    type: "get",
    contentType: "application/json",
    data: params,
    success: function(response) {
      renderItems(response)
    }
  });
}

// Render the items on the page
function renderItems(response) {
  const search_container = document.getElementById("search-results");
  const db_container = document.getElementById("db-results");
  
  $("#placeholders").hide()
  
  renderContainer(search_container, response.search_results, true);
  renderContainer(db_container, response.db_results, true);

  $(".item-score-input").on("keydown", function(e) {if (e.key == "Enter") sendSaveRequest(e);});
  $(".item-save").click(function(e) {sendSaveRequest(e)});
  $(".item-remove").click(function(e) {sendRemoveRequest(e)});
}

function sendSaveRequest(e) {
  const item = e.currentTarget.parentElement;
  const input = item.querySelector(".item-score-input");
  let data = item.data;
  data.score = input.value;
  $.ajax({
    url: "",
    type: "post",
    contentType: "application/json",
    data: JSON.stringify(data),
    success: function(response) {
      alert(response);
    }
  });
}

function sendRemoveRequest(e) {
  const item = e.currentTarget.parentElement;
  item.style.display = "none";
  let data = item.data;
  data.score = "";
  $.ajax({
    url: "",
    type: "post",
    contentType: "application/json",
    data: JSON.stringify(data),
    success: function(response) {
      alert(response);
    }
  });
}

