$(document).ready(function(){
	
	var room_in=$('#room_in').val()
	$('#id_room').val(room_in);
	var place_in=$('#place_in').val()
	$('#id_place').append($('<option></option>').attr("value",place_in).text(place_in));			
	var place_num_in=$('#place_num_in').val()
	$('#id_place_num').append($('<option></option>').attr("value",place_num_in).text(place_num_in));	
	print_local()
		
	$('#id_local').attr('disabled','true');
	
	$('#id_room').on('change',function () {
			room=$('#id_room').val();
			filter_loc(room,'');
			
	
	});
	
	$('#id_place').on('change',function () {
			room=$('#id_room').val();
			place=$('#id_place option:selected').text();
			console.log(place)
			filter_loc(room,place);
			
				
	});
	
	$('#id_place_num').on('change',function () {
			print_local()
			
			});
	
	function print_local() {
			room=$('#id_room').val();
			place=$('#id_place option:selected').text();
			num=$('#id_place_num option:selected').text()
			$('#id_local').val(room+'-'+place+'-'+num);
			
	
	}
	
	
	function filter_loc(room,place) {
		console.log('finding started');
		$.ajax({
			url :'/item_loc_filter/',
			type : "POST",
			data : {room:room,place:place},
			
			success : function(json) {
				console.log(json);
				console.log('success');
				if (place=='') {
					$('#id_place')
						.find('option')
						.remove()
						.end()
					
					$.each(json, function (index,name) {
							$('#id_place')			
							.append($('<option></option>').attr("value",name).text(name));			
							});
					$('#id_place').val("");
					print_local()
				}
				else {
					$('#id_place_num')
						.find('option')
						.remove()
						.end()
					
					$.each(json, function (index,name) {
							$('#id_place_num')			
							.append($('<option></option>').attr("value",name).text(name));			
							});
					$('#id_place_num').val("");
					print_local();
				};
				
				
				},
				
			error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText)
            
            }
				
			
		});
		
		
	};
	


	

	

	
	
	

	
	
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
	
}) 
