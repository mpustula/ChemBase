
$(document).ready(function(){

	$('#names_ctrl').on('click', function() {
		$('#names_block').slideToggle(500);
	});

	$('#str_ctrl').on('click', function() {
		$('#str_block').slideToggle(500);
	});

	$('#prop_ctrl').on('click', function() {
		$('#prop_block').slideToggle(500);
	});

	$('#safety_ctrl').on('click', function() {
		$('#safety_block').slideToggle(500);
	});

	$('#risk_ctrl').on('click', function() {
		$('#risk_block').slideToggle(500);
	});

	$('#editor').on('click',function(){
		var mol_text=$('#id_molfile').val();
		fetch_image(mol_text);
	});


	$('#save_form').on('click', function(event){
		event.preventDefault();
		var cmpd_name=$('#id_name').val();
		var name_valid="False";
		if (cmpd_name==="") {
			console.log('No compound name is given');
			$('#name_field').addClass("error_highlight");
			$('#name_error_text').html("This field is required");
			name_valid="False"
		} else {
            $('#name_field').removeClass("error_highlight");
            $('#name_error_text').html("");
            name_valid="True"
        }
		var str_valid="False"
		var fetch_properties=$.ajax({
			url: '/properties_ajax/',
			type: "POST",
			data: {mol: $('#id_molfile').val()}
			});
		fetch_properties.then(
			function() {
				console.log('Structure validation OK');
				$('#str_block').removeClass("error_highlight");
				$('#structure_error_text').html("");
				if (name_valid==="True") {
					$('#cmpd_exp_form').submit();
				}

			},
			function () {
				console.log('Validation error - wrong structure');
				$('#str_block').addClass("error_highlight");
				$('#structure_error_text').html("Validation error: The structure provided here does not represent any correct chemical structure.");

			}
		);

	});


	function fetch_image(molfile_text) {
		console.log('finding started');
		$.ajax({
			url :'/image_ajax/',
			type : "POST",
			data : {mol : molfile_text},

			success : function(json) {
				console.log(json);
				console.log('success');

				var image=json['image'];
				console.log(image);
				$('#new_str_id').attr('src',image);
				$('#id_image').val(image);
				},

			error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText)
            }
		});

	}

	function write_properties(json) {
		var form=json['formula'];
		console.log(form);
		$('#id_formula').val(form);
		$('#id_weight').val(json['mass']);
		$('#id_smiles').val(json['smiles']);
		$('#id_inchi').val(json['inchi'])
	}


	$('#properties').on('click', function(event) {
		event.preventDefault();
		var fetch_properties=$.ajax({
			url: '/properties_ajax/',
			type: "POST",
			data: {mol: $('#id_molfile').val()}
		});
		fetch_properties.then(function(value) {
			console.log('success');
			console.log(value);
			write_properties(value)}, function () {console.log('error')
		}
		);
	});

	$('#formula_clean').on('click', function(event) {
		event.preventDefault();
		$.ajax({
			url :'/formula_ajax/',
			type : "POST",
			data : {formula : $('#id_formula').val()},

			success : function(json) {
				console.log(json);
				console.log('success');

				var form=json['new_formula'];
				console.log(form);
				$('#id_formula').val(form);
				},

			error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText)

            }


		});

	});

	$('#clean_str').on('click', function(event) {
		event.preventDefault();
		$.ajax({
			url :'/clean_str_ajax/',
			type : "POST",
			data : {mol: $('#id_molfile').val()},

			success : function(json) {
				console.log(json);
				console.log('success');

				$('#id_molfile').val(json['new_mol'])
				},

			error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText)

            }


		});

	});





//	$('#str_chemspider').on('click', function() {
//		fetch_structure();
//
//	});







///--------------------------------------------------------------------------------------------------------------------

	/////Adding csrf token

$(function() {


    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

	});

///----------------------------------------------------------------



});


