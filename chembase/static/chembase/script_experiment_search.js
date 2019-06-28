$(document).ready(function() {

$("#id_text").autocomplete({
    source: "/experiments/search/ajax",
    minLength: 2,
    open: function(){
        setTimeout(function () {
            $('.ui-autocomplete').css('z-index', 99);
        }, 0);
    }
  });


})