import { getRadioSelected } from "./search.js";

$(document).ready(function() {
  $(".depth").click(function() {
    window.setTimeout(updateAnalysisDesc, 10);
  });

  $("#generate-analysis-button").click(function() {
    generateAnalysis();
  });
});

function updateAnalysisDesc() {
  const count = document.getElementById("generate-analysis-count");
  const desc = document.getElementById("generate-analysis-desc");
  const depth = getRadioSelected(document.getElementsByName("analysis-depth"));
  if (depth === "100") {
    count.innerText = "100";
    desc.innerText = "Short analysis, should only take a few seconds.";
  }
  else if (depth === "250") {
    count.innerText = "250";
    desc.innerText = "Standard analysis, should't take too long.";
  }
  else if (depth === "500") {
    count.innerText = "500";
    desc.innerText = "Long analysis, may take some time.";
  }
  else if (depth === "1000") {
    count.innerText = "1000";
    desc.innerText = "Extended analysis, may take a few minutes.";
  }
  else if (depth === "5000") {
    count.innerText = "5000";
    desc.innerText = "Extreme analysis, could take a VERY long time.";
  }
  else  {
    count.innerText = "Invalid";
    desc.innerText = "Invalid analysis depth, please reload the page.";
  }
}

function generateAnalysis() {
  $("#generate-analysis-loading").removeClass("border")
  $("#generate-analysis-loading").removeClass("border-secondary")
  $("#generate-analysis-loading").addClass("spinner-border")
  $("#generate-analysis-button").hide()
  const depth = getRadioSelected(document.getElementsByName("analysis-depth"));
  window.location.href="/stats?depth="+depth;
}