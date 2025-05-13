import { addClassTo } from "./util.js";

// Create the items and append the items to the container
export function renderContainer(container, items) {
  for (let i in items) {
    const item = createItem(items[i]);
    container.appendChild(item, i);
  }
}

// Create an item from data
function createItem(data, addSave) {
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
  if (addSave) {
    let button = document.createElement("button");
    button.type = "button";
    addClassTo(button,"item-save col-2 col-lg-1 btn btn-secondary");
    button.innerText = "Save";
    item.appendChild(button);
  }
  
  return item;
}