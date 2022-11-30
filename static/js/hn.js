function sortStories() {
  var sortComboBox = document.getElementById("sort-stories-combobox");
  var selectedValue = sortComboBox[sortComboBox.selectedIndex].value;
  console.log("Selected value " + selectedValue);
  switch (selectedValue) {
    case "time":
    case "score":
    case "descendants":
    case "ratio":
      const urlParams = new URLSearchParams(window.location.search);
      urlParams.set("order_by", selectedValue);
      window.location.search = urlParams;
      break;
  }
}

function exportStories() {
  console.log("exporting stories");
  window.location = "export";
}

function clearSaved() {
  console.log("Clear saved stories");
  window.location = "clear_saved";
}

function getCookie(c_name) {
  if (document.cookie.length > 0) {
    c_start = document.cookie.indexOf(c_name + "=");
    if (c_start != -1) {
      c_start = c_start + c_name.length + 1;
      c_end = document.cookie.indexOf(";", c_start);
      if (c_end == -1) c_end = document.cookie.length;
      return unescape(document.cookie.substring(c_start, c_end));
    }
  }
  return "";
}
function hideAll() {
  let stories = document.getElementsByClassName("hnr-a");
  let ids = [];
  for (s of stories) {
    ids.push(s.getAttribute("id"));
  }
  console.log(ids);

  fetch("hide_all", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ ids: ids }),
  }).then(() => {
    window.location.reload();
  });
}

function getStoryId(element) {
  let li = element.closest("li");
  if (li == null) {
    return;
  }
  return li.getAttribute("id");
}
function doRequest(request_name, request_body) {
    return fetch(request_name, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: request_body,
      });
}
async function hideStory(element) {
  console.log("hide story ", element);
  let id = getStoryId(element);
  let body = JSON.stringify({
    id: id,
    hide: true,
  });

  let response = await doRequest("hide_story", body);

  if (response.status == 200) {
    element.closest("li").hidden = true;
  }
  console.log(response);
}

async function unhideStory(element) {
  console.log("unhide story ", element);
  let id = getStoryId(element);
  let body = JSON.stringify({
    id: id,
    hide: false,
  });

  let response = await doRequest("hide_story", body);

  if (response.status == 200) {
    element.closest("li").hidden = true;
  }
  console.log(response);
}

async function saveStory(element) {
  console.log("save story: ", element);
  let id = getStoryId(element);
  let parent = element.parentNode;

  let response = await doRequest("save_story", JSON.stringify({ id: id }));

  if (response.status == 200) {
    let hide_element = element.cloneNode(true);
    console.log("clone: ", hide_element);
    hide_element.setAttribute(
      "class",
      "link-button hnr-del-icon fa-solid fa-square-minus fa-xl"
    );
    hide_element.setAttribute("onclick", "deleteStory(this)");
    parent.replaceChild(hide_element, element);
    console.log(response);
  }
}

async function deleteStory(element) {
  console.log("Delete story: ", element);
  let id = getStoryId(element);
  let parent = element.parentNode;

  let response = await doRequest("delete_story", JSON.stringify({ id: id }));

  if (response.status == 200) {
    let save_element = element.cloneNode(true);
    console.log("clone: ", save_element);
    save_element.setAttribute(
      "class",
      "link-button hnr-add-icon fa-solid fa-square-plus fa-xl"
    );
    save_element.setAttribute("onclick", "saveStory(this)");
    parent.replaceChild(save_element, element);
    console.log(response);
  }
}
