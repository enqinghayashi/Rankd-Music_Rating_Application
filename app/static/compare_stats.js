import { getSelectedFriend } from "./friend_select.js";

$(document).ready(function() {
  $("#friend-select").change(function() {
    window.setTimeout(changeAnalysis, 10); // Timeout for 10ms before calling to give time for options to update
  })
});

function changeAnalysis() {
  window.location.href="/compare_stats?friend_id="+getSelectedFriend()
}