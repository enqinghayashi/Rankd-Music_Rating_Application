$(document).ready(function() {
  /*
  This causes the event to be triggered twice even though stopPropagation should fix that
  $("#search-bar-input").on("keydown", function(e) {
    if (e.key == "Enter") getItems();
    e.stopPropagation();
  });
  */
  $(".filter").click(function() {
    window.setTimeout(getItems, 10); // Timeout for 10ms before calling to give time for options to update
  });

  getItems();
});

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
  const params = {
    "search": search,
    "type": type,
    "saved": saved
  };
  return params;
}

// Make a request to the server for the items
function getItems() {
  $("#search-results").empty()
  $("#db-results").empty()
  $("#placeholders").show()
  
  const params = getSearchParameters();
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
  // We don't want to empty the containers every time, this will be specified in the response
  
  renderContainer(search_container, response.search_results);
  renderContainer(db_container, response.db_results);

  $(".item-score-input").on("keydown", function(e) {if (e.key == "Enter") send_save_request(e);});
  $(".item-save").click(function(e) {send_save_request(e)});
}

function send_save_request(e) {
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

// Create the items and append the items to the container
function renderContainer(container, items) {
  for (let i in items) {
    const item = createItem(items[i]);
    container.appendChild(item, i);
  }
}

// Create an item from data
function createItem(data) {
  // Container
  let item = document.createElement("div");
  addClassTo(item, "item item-type-" + data.type);
  item.data = data;
 
  // Rating input
  let input = document.createElement("input");
  input.type = "text";
  addClassTo(input, "item-score-input col-2 col-lg-1");
  input.placeholder = "/10";
  input.value = data.score;
  item.appendChild(input);

  // Img
  let img = document.createElement("img");
  addClassTo(img, "item-img");
  img.src = data.img_url;
  img.alt = data.title;
  item.appendChild(img);
  
  // Description
  let desc = document.createElement("div");
  addClassTo(desc, "item-desc col");
  
  let title = document.createElement("p");
  addClassTo(title, "item-title");
  title.innerText = data.title;
  desc.appendChild(title);
  
  if (data.type !== "artist") {
    let creator = document.createElement("p");
    addClassTo(creator, "item-creator");
    creator.innerText = data.creator;
    desc.appendChild(creator);
  }
  
  item.appendChild(desc);

  // Save Button
  let button = document.createElement("button");
  button.type = "button";
  addClassTo(button,"item-save col-2 col-lg-1 btn btn-secondary");
  button.innerText = "Save";
  item.appendChild(button);

  return item;
}

function addClassTo(item, class_str) {
  const classes = class_str.split(" ")
  for (let i in classes) {
    item.classList.add(classes[i])
  }
}