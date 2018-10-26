$(document).ready(function(){
	
	var room_in=$('#room_in').val()
	$('#id_room').val(room_in);
	var place_in=$('#place_in').val()
	$('#id_place').append($('<option></option>').attr("value",place_in).text(place_in));			
	var place_num_in=$('#place_num_in').val()
	$('#id_place_num').append($('<option></option>').attr("value",place_num_in).text(place_num_in));	
	print_local()
	
	
	var cmpd_id=$('#cmpd_id_input').val();
	var owner=$('#id_owner').val();
	fetch_orz(cmpd_id,owner);
		
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
			
	$('#id_owner').on('change',function () {
			var cmpd_id=$('#cmpd_id_input').val();
			var owner=$('#id_owner').val();
			fetch_orz(cmpd_id,owner)
			
			});
			
	$('#suggestions').on('click', function(event) {
			event.preventDefault();
			var cmpd_id=$('#cmpd_id_input').val()
			console.log(cmpd_id);
			fetch_suggestions(cmpd_id,false);
			$('#suggestions_div').slideDown(500);
			
	
	});
	
	function print_local() {
			room=$('#id_room').val();
			place=$('#id_place option:selected').text();
			num=$('#id_place_num option:selected').text()
			$('#id_local').val(room+'-'+place+'-'+num);
			
	
	}
	
	function fetch_orz(cmpd_id,owner_id) {
		$.ajax({
			url :'/item_orz/',
			type : "GET",
			data : {"cmpd_id":cmpd_id,"owner_id":owner_id},
			
			success : function(json) {
				console.log(json);
				$('#id_dailyused').val(json['du']);
				if (json['ewid']==true) {$('#id_ewid').prop("checked",true);console.log('true')}
				else  {$('#id_ewid').prop("checked",false)};
				if (json['resp']==true) {$('#id_resp').prop("checked",true)}
				else {$('#id_resp').prop("checked",false)};
				
				},
					
			error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText)
            
            },
				
			
		});
		
		
	};	
	
	function fetch_suggestions(cmpd_id,ignore_temp) {
		var owner=$('#id_owner option:selected').text();
		$.ajax({
			url :'/sug/loc/cmpd/',
			type : "GET",
			data : {"cmpd_id":cmpd_id,"owner":owner,"ignore_temp":ignore_temp},
			
			success : function(json) {
				console.log(json);
				var exist=json['existing']
				var html=''
				if (exist.length>0) {
					html=html+'<p>The following items of this compound already exists:</p>';
					$.each(exist, function (index,name) {
						html=html+"<p class='items_location'>"+name+"</p>";
						});
				}
				var del=json['deleted']
				if (del.length>0) {
					html=html+'<hr class="suggestions_hr"><p>The old entries of this compound have been found:</p>';
					$.each(del, function (index,name) {
						html=html+"<p class='items_location'>"+name+"</p>";
						});
					html=html+'<p>Instead of adding a new item you may <a href="/cmpd/'+cmpd_id+'">restore one of the old ones</a> </p>'
				}
				var group=json['group']
				var group_name=json['group_name']
				var st_temp=json['st_temp']
				if (group.length>0) {
					html=html+'<hr class="suggestions_hr"><p>The other compounds from group "'+group_name+'" are located as follows:</p>';
					html=html+'<table id="items_table" class="group_items"><tr><th>Location</th><th>Number of compounds</th></tr>'
					$.each(group, function (index,name) {
						html=html+"<tr><td>"+name[0]+"</td><td>"+name[1]+"</td></tr>";
						});
					html=html+"</table>"
					if (st_temp!="" & ignore_temp==false) {html=html+'<p id="temp_warning">The table above includes only compounds with storage temperature "'+st_temp+'" <a id="temp_link" href="">Click here to show locations for any temperature.</a>'}
				}
				$('#suggestions_div').html(html);
				if (st_temp!="") {
						$('#temp_link').on('click', function(event) {
							event.preventDefault();
							var cmpd_id=$('#cmpd_id_input').val()
							fetch_suggestions(cmpd_id,true);
							});				
				
				};
				
				},
				
			error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText)
            
            }
				
			
		});
		
		
	};	
	
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
