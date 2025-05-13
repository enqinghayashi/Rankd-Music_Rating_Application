export function addClassTo(item, class_str) {
  const classes = class_str.split(" ")
  for (let i in classes) {
    item.classList.add(classes[i])
  }
}