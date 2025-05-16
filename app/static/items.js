import { addClassTo } from "./util.js";

// Create the items and append the items to the container
export function renderContainer(container, items, addSave) {
  for (let i in items) {
    const item = createItem(items[i], addSave);
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

  // Save and Delete Button
  if (addSave) {
    let save = document.createElement("button");
    save.type = "button";
    addClassTo(save,"item-save col-2 col-lg-1 btn btn-secondary me-2");
    save.innerText = "Save";
    item.appendChild(save);

    let remove = document.createElement("button");
    remove.type = "button";
    addClassTo(remove,"item-remove btn btn-danger");
    let remove_icon = document.createElement("i");
    addClassTo(remove_icon, "bi bi-trash")
    remove.appendChild(remove_icon);
    item.appendChild(remove);
  }
  
  return item;
}