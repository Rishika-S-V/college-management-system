// $(".input-pass__eye-icon").click(function() {

//     $(this).toggleClass("far fa-eye-slash");

//     var input = $($(this).attr("toggle"));
//     if (input.attr("type") == "password") {
//         input.attr("type", "text")
//     } else {
//         input.attr("type", "password")
//     }
// });

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