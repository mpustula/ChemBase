$(document).ready(function(){


$('#perm_guide').on('click', function (event) {
	event.preventDefault();
	//$('#perm_info').slideDown(500);
	$('#perm_info').show();

});


$('#new_ctrl').on('click', function () {
	$('#new_mail').slideToggle(500);
})

$('#test_mail').on('click', function () {
	$('#mail_testing').slideToggle(500);
})



$('#close_modal').on('click', function () {
	$('#perm_info').hide();
});

$('#reset_pass').on('click', function () {
	var user_id=$('#user_id_id').val();
	console.log(user_id);
	send_password_reset_request(user_id);

})

$('#send_test').on('click', function() {
	var test_addr = $('#test_address').val()
	console.log(test_addr)
	if (test_addr !== '') {
		$('#test_result').html("<p class='info'>Please waite while the test message is being prepared...</p>");
		send_test_mail(test_addr)
	}
})

$('#test_chemspider').on('click', function() {
	$('#test_ch_result').html("<p class='success'>Sending chemspider request for compound id 2157...</p>");
	test_chemspider()
})


function test_chemspider() {
	console.log('testing started');
	$.ajax({
		url :'/admin/test_chemspider',
		type : "POST",
		data : {},

		success : function(ans) {
			console.log(ans);
			console.log('success');

			$('#test_ch_result').html("<p class='success'>"+ans+"</p>");
			//$('#wait_box').fadeOut('fasf',function(){$('#orz_input').fadeIn('fast')});
				},

		error : function(xhr,errmsg,err) {
			console.log(xhr.status + ": " + xhr.responseText);
			var error_p="<p class='warning'> Error. Server response: "+xhr.status + ": " + xhr.responseText+"</p>"
			//$('#wait_box').fadeOut('fasf',function(){$('#orz_input').fadeIn('fast')});
			$('#test_ch_result').html(error_p);
		}


	});


};



function send_test_mail(address) {
	console.log('sending started');
	$.ajax({
		url :'/admin/test_mail',
		type : "POST",
		data : {'address': address},

		success : function(ans) {
			console.log(ans);
			console.log('success');

			$('#test_result').html("<p class='success'>"+ans+"</p>");
			//$('#wait_box').fadeOut('fasf',function(){$('#orz_input').fadeIn('fast')});
				},

		error : function(xhr,errmsg,err) {
			console.log(xhr.status + ": " + xhr.responseText);
			var error_p="<p class='warning'> Error. Server response: "+xhr.status + ": " + xhr.responseText+"</p>"
			//$('#wait_box').fadeOut('fasf',function(){$('#orz_input').fadeIn('fast')});
			$('#test_result').html(error_p);
		}


	});


};


function send_password_reset_request(user) {
		console.log('sending started');
		$.ajax({
			url :'/admin/reset_password',
			type : "POST",
			data : {'user_id': user},
			
			success : function(json) {
				console.log(json);
				console.log('success');
				
				
				$('#password_reset').append("<p class='success'>New password has been sent</p>");
				//$('#wait_box').fadeOut('fasf',function(){$('#orz_input').fadeIn('fast')});
	
					},		
				
			error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
            var error_p="<p class='warning'> Error. Server response: "+xhr.status + ": " + xhr.responseText+"</p>"
            //$('#wait_box').fadeOut('fasf',function(){$('#orz_input').fadeIn('fast')});
            $('#password_reset').append(error_p);
            }
				
			
		});
		
		
	};
	
	
$('#expiry_form').on('submit', function (event) {
	event.preventDefault();
	var users=$('#id_users').val();
	var date=$('#id_exp_date').val();
	var if_mail=$('#id_if_mail').prop( "checked" );
	console.log(date);
	console.log(if_mail);
	$('#exp_submit').prop('disabled', true);
	$.each(users, function(index,value) {
			//console.log(index+':'+value)
			console.log(index);
			console.log(value);
			send_password_expiry_request(value,date,if_mail);
			
		});
	
	
});


function send_password_expiry_request(user,date,mail) {

		console.log('sending started');
		$.ajax({
			url :'/admin/user/expire',
			type : "POST",
			data : {'user_id': user,'date':date,'if_mail':mail},
			
			success : function(xhr) {
				console.log(xhr);
				$('#server_responses').append("<p class='success'>"+xhr+"</p>");
	
					},		
				
			error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
            var error_p="<p class='warning'> Error. Server response: "+xhr.status + ": " + xhr.responseText+"</p>"
            $('#server_responses').append(error_p);
            }
		});
	};


//window.onclick = function(event) {
//	if (event.target==$('#perm_info')) {
//	$('#perm_info').hide()}
//};


$('#id_is_staff').on('change', function () {staff_warning()});
$('#id_user_permissions').on('change', function () {staff_warning()});
$('#id_is_superuser').on('change', function () {staff_warning()});

function staff_warning() {
	var is_staff=$('#id_is_staff').prop('checked');
	var is_su=$('#id_is_superuser').prop('checked');
	var perms=$('#id_user_permissions option:selected').text();
	if (is_su==false) {
		if (is_staff==true) {
			if (perms.indexOf('auth') >= 0) {
				$('#staff_error').html('<p  class="error">Warning! Granting user account with "Staff" attribute and "auth" type privileges may be in some cases used to create a superuser account!</p>')
			}
			else {$('#staff_error').html('<p  class="notice">Notice - staff attribute allows user to log into Django admin site and manipulate objects manually. Use with care.</p>')}
			}
		else {
			$('#staff_error').html('')
		}
	}
	else {
			$('#staff_error').html('')
	}

};

function fetch_dels() {
var del_buttons=$('#perm_table').find('input');
console.log(del_buttons);
del_buttons.each(function () {//$(this).on('click',function () {
						var row_id=$(this).attr('num');
						$(this).on('click',function () {					
						console.log(row_id);
						$('#perm_table > tbody > tr#'+row_id).remove();
					});
	});
}

 function add_perm() {
 		var group_id=$('#id_group').val();
 		var group_name=$('#id_group option:selected').text();
 		var perm_id=$('#id_permission').val();
 		var perm_name=$('#id_permission option:selected').text();
 		var row_id=group_id+"-"+perm_id
 		var html_to_append="<tr id="+row_id+"><td>#</td>"+
		'<td><input class="perm_code" type="text" name="perm_code_" value='+row_id+' /></td>'+
		'<td>'+group_name+'</td>'+
		'<td>'+perm_name+'</td>'+
		"<td><input class='small' id='del_perm' type='button' value='Delete' num="+row_id+" /></td>"+
		"</tr>";
		if ($('tr#'+row_id).length == 0)
		{
 		$('#perm_table > tbody:last-child').append(html_to_append);
		fetch_dels()
 		}	
 		
 		};
 		
 		
function check_passwords() {
		var pass1=$('#id_password').val();
		var pass2=$('#id_password_commit').val();
		var error=''
		if (pass1 == '')
			{ error='You must set the password' }
		else {
			if (pass1 != pass2)
				{error = 'The passwords are not the same!';
				$('#user_submit').prop('disabled',true);
				}
			else {
				$('#user_submit').prop('disabled',false)
				}
							
			}
		
		$('#pass_error').html(error)
}
 		
		
fetch_dels();	
$('#save_perm').on('click', function () {
 		add_perm()
 	 	
 	});
 	
$('#new_perm').on('click',function () {$('#edit_permission').slideToggle(500) });

$('#id_password').on('change', function () {check_passwords()});
$('#id_password_commit').on('change', function () {check_passwords()});
	
	
	
	
	
	
	
	
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
