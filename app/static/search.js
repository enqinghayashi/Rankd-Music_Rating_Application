// Return the id of the selected radio button
function getRadioSelected(radios) {
  for (let i in radios) {
    const radio = radios[i];
    if (radio.checked) return radio.id;
  }
}

// Get the contents of the search bar and search options
export function getSearchParameters() {
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