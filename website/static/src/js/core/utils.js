/**
 *
 * @param {HTMLFormElement} form
 * @return {Object}
 */
function get_form_values(form) {
  var elements = form.elements;
  var radio_name=null;
  var data = {};
  for (var i = 0; i < elements.length; i++) {
    var item = elements.item(i);
    if (item.tagName == "INPUT") {
      if (item.type == "radio") {
        if (radio_name==null) {
          radio_name=item.name;
        }
      }
      data[item.name] = item.value;
    }
  }
  /**@type {HTMLInputElement} */
  var radio_btn = document.querySelector(
    `input[type='radio'][name=${radio_name}]:checked`
  );
  data[radio_btn.name] = radio_btn.value;
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
