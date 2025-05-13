import { renderContainer } from "./items.js";
import { getSearchParameters } from "./search.js";
import { getSelectedFriend } from "./friend_select.js";

$(document).ready(function() {
  $("#search-bar-input").on("keydown", function(e) {
    if (e.key == "Enter") getItems();
    e.stopPropagation();
  });
  
  $(".filter").click(function() {
    window.setTimeout(getItems, 10); // Timeout for 10ms before calling to give time for options to update
  });

  $("#friend-select").change(function() {
    window.setTimeout(getItems, 10); // Timeout for 10ms before calling to give time for options to update
  })

  $("#saved").hide(); // Lazy way of removing the save button without breaking other js
  $("[for=saved]").hide()

  getItems();
});

function getItems() {
  console.log("TESTING")
  $("#user-items").empty();
  $("#friend-items").empty();
  
  const params = getSearchParameters();
  params["friend_id"] = getSelectedFriend();
  console.log(params);
  requestItems(params);
}

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

function renderItems(response) {
  const user_container = document.getElementById("user-items")
  const friend_container = document.getElementById("friend-items")

  renderContainer(user_container, response.user_results);
  renderContainer(friend_container, response.friend_results);
}
