
/**
 * 
 * @param {HTMLFormElement} form 
 * @param {SubmitEvent} event 
 */
function submit_form(form, event){
    event.preventDefault();

    const btn = form.querySelector("button");
    const old_class = btn.className;
    const old_innertext = btn.innerText;
  
    btn.className = "btn btn--capsule btn--disabled";
    btn.innerText = "Please Wait...";

    const form_value = get_form_values(form);
    console.log(form_value)

    const api_data = backend_api("/common/login-val", form_value)
    api_data.then((d)=>{
        console.log(d)
    })
}

