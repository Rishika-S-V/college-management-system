/**
 *
 * @param {HTMLFormElement} form
 * @return {Object}
 */
 function get_form_values(form) {
  var elements = form.elements;
  var data = {};
  var radio_btn_groups = [];
  var check_box_groups = [];

  for (var i = 0; i < elements.length; i++) {
      var item = elements.item(i);

      if (item.tagName == "INPUT" || item.tagName == "SELECT") {
          if (item.type == "radio") {
              if (!radio_btn_groups.includes(item.name)) {
                  radio_btn_groups.push(item.name);
              }
              continue;
          }
          if (item.type == "checkbox") {
              if (!check_box_groups.includes(item.name)) {
                  check_box_groups.push(item.name);
              }
              continue;
          }
          data[item.name] = item.value;
      }
  }

  radio_btn_groups.forEach((val) => {
      /**@type {HTMLInputElement} */
      var radio_btn = document.querySelector(
          `input[type='radio'][name=${val}]:checked`
      );
      data[val] = radio_btn == null ? "" : radio_btn.value;
  });

  check_box_groups.forEach((val) => {
      /**@type {NodeList} */
      var check_boxes = document.querySelectorAll(
          `input[type='checkbox'][name=${val}]:checked`
      );
      var checked_values = [];
      
      check_boxes.forEach((check_box) => {
        checked_values.push(check_box.value)
      });

      data[val] = checked_values;
  });

  return data;
}

/**
 * @param {string} url
 * @param {Object} args
 * @type {Promise}
 */
async function backend_api(url, args) {
  const fetched_data = await fetch(url, {
    method: "POST",
    body: JSON.stringify(args),
  });

  /**@type {Promise} */
  var json_data = await fetched_data.json();

  return json_data;
}

function eye_toggle(element, event) {
    var cls = element.className;
    var inp = element.previousElementSibling.previousElementSibling
    if (cls == "fas fa-eye input-pass__eye-icon"){
        element.className = "fas fa-eye-slash input-pass__eye-icon"
        inp.type = "text"
    } else if(cls == "fas fa-eye-slash input-pass__eye-icon"){
        element.className = "fas fa-eye input-pass__eye-icon"
        inp.type = "password"
    }
}
