function get_form_values(form) {
    var elements = form.elements;
    var radio_name = "roles-input";
    var data = {};
    for (var i = 0; i < elements.length; i++) {
        var item = elements.item(i);
        if (item.tagName == "INPUT") {
            if (item.type == "radio") {
                if (radio_name == "roles-input") {
                    radio_name = item.name;
                }
                else if (radio_name == "roles-input") {
                    
                    // var item1 = elements.item(i);
                    radio_name = item.name;
                    alert(radio.name);
                }
                else if (radio_name =="roles-input") {
                    // var item2 = elements.item(i);
                    radio_name = item.name;
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