$(document).ready(function(){


$('#perm_guide').on('click', function (event) {
	event.preventDefault();
	//$('#perm_info').slideDown(500);
	$('#perm_info').show();


});

$('#close_modal').on('click', function () {
	$('#perm_info').hide();
});

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
	
	
}) 
