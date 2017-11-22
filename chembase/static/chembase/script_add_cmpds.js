
function fetch_structure() {
		console.log('finding started');
		$.ajax({
			url :'/structure_ajax/',
			type : "POST",
			data : {csid : $('#id_csid').val()},
			
			success : function(json) {
				console.log(json);
				console.log('success');
				
				var molecule=json['molfile'];
				console.log(molecule);
				$('#id_molfile').val(molecule);
				},
				
			error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText)
            
            }
				
			
		});
		
		
	};
	
function display_ghs_classes(array,values_dict) {
			var html_code='';
			console.log(array);
			console.log(values_dict);
			$.each(array, function(index,value) {
				var input_name='id_class_'+index;
				console.log(input_name);
				var input_val=values_dict[input_name];
				if (typeof input_val == "undefined") {    						
						input_val=''
    												}
				line='<span class="hazard_item">'+value+', category: <input type="text" value="'+input_val+'" name="id_class_'+index+'" /></span>';
				html_code=html_code+line;
				});
			$('#risk_classes_categories').html(html_code);	
	
	};
	
	

$(document).ready(function(){
	
	read_pictograms()
	
	
	var classes_start=$('#id_class_extr').val();
	var dict_c=$('#id_classes_dict').val();
	//transl_ghs(classes_start,dict_c);
	
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
	
	
	$('#id_pictograms').on('change',function(){
		var picts=$(this).val();
		read_pictograms();
	});
	
	function read_pictograms() {
		var picts=$('#id_pictograms').val();
		//console.log(picts);
		$('#pictograms_frame').empty();
		$.each(picts, function(index,value) {
			//console.log(index+':'+value)
			$('#pictograms_frame').append("<img class='pictograms' src='/static/chembase/data/pict/GHS0"+value+".svg' />")
		});
	};
	
	$('#chemspider').on('click',function(){
		var csid_num=$('#id_csid').val();
		fetch_image(csid_num,'');
	});
	
	$('#editor').on('click',function(){
		var mol_text=$('#id_molfile').val();
		fetch_image('',mol_text);
	});
	
	function fetch_image(csid_num,molfile_text) {
		console.log('finding started');
		$.ajax({
			url :'/image_ajax/',
			type : "POST",
			data : {csid : csid_num, mol : molfile_text},
			
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
	
	function transl_ghs(array,values_dict) {
		$.ajax({
			url :'/ghs_class_ajax/',
			type : "POST",
			data : {'array' : array.toString()},
			
			success : function(json) {
				console.log(json);
				console.log(values_dict);
				display_ghs_classes(json,values_dict);
				},
				
			error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText)
            
            }
				
			
		});
	};
	
	
	$('#id_class_extr').on('change', function () {
		var classes=$('#id_class_extr').val();
		var inputs=$('#risk_classes_categories').find('input');
		var map={}
		inputs.each(function() {
			map[$(this).attr('name')]=$(this).val();
			});
		$('#risk_classes_categories').html('')
		transl_ghs(classes,map)	
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
	
	$('#id_sds_file').on('change', function () {
		var file_to_sent=$('#id_sds_file')[0].files[0]
		console.log(file_to_sent);
		console.log(file_to_sent['name']);
		$('#sds_path_field').val(file_to_sent['name']);
	
	});
	

	
	$('#sds_extr').on('click', function () {
		var file_to_sent=$('#id_sds_file')[0].files[0];
		var formData = new FormData();
		formData.append("sds_file", file_to_sent);
		$.ajax({
			url :'/sds_ajax/',
			type : "POST",
			data : formData,
			processData: false,//https://stackoverflow.com/questions/6974684/how-to-send-formdata-objects-with-ajax-requests-in-jquery//
  			contentType: false,
			success : function(json) {
				console.log(json);
				var picts_new=json['pict_list'];
				$('#id_pictograms').val([]);
				$('#id_pictograms').val(picts_new);
				$('#id_pictograms').select2('destroy');
				$('#id_pictograms').select2();
				read_pictograms();

				$('#id_sds_name').val(json['name']);
				$('#id_sds_cas').val(json['cas']);
				$('#id_warning').val(json['signal']);
				$('#id_h_numbers').val(json['H']);
				$('#id_h_text').val(json['H_text']);
				$('#id_p_numbers').val(json['P']);
				$('#id_p_text').val(json['P_text']);
				
				$('#id_adr_num').val(json['adr_num']);
				$('#id_adr_class').val(json['adr_class']);
				$('#id_adr_group').val(json['adr_group']);
				
				$('#id_classification').val(json['clas_text']);
				var risk_classes_dict=json['clas_extr'];
				console.log(risk_classes_dict)
				console.log(Object.keys(risk_classes_dict));
				map_new={};
				$.each(risk_classes_dict, function(index,value) {
					map_new['id_class_'+index]=value;
					});
				$('#id_class_extr').val(Object.keys(risk_classes_dict));
				$('#id_class_extr').select2('destroy');
				$('#id_class_extr').select2();
				var classes_new=$('#id_class_extr').val();
				console.log(classes_new);
				transl_ghs(classes_new,map_new)
				
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

	 
