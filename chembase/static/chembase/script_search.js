
$(document).ready(function(){

function fetch_dels() {
var del_buttons=$('#class_table').find('input');
console.log(del_buttons);
del_buttons.each(function () {//$(this).on('click',function () {
						var row_id=$(this).attr('num');
						$(this).on('click',function () {					
						console.log(row_id);
						$('#class_table > tbody > tr#'+row_id).remove();
					});
	});
}
	

 function add_class() {
 		var class_id=$('#id_ghs_class').val();
 		var class_name=$('#id_ghs_class option:selected').text();
 		var category=$('#id_number').val();
 		var row_id=class_id+"-"+category
 		var html_to_append="<tr id="+row_id+">"+
		'<td><input class="perm_code" type="text" name="class_code_" value='+row_id+' /></td>'+
		'<td>'+class_name+'</td>'+
		'<td>'+category+'</td>'+
		"<td><input class='small' id='del_perm' type='button' value='Delete' num="+row_id+" /></td>"+
		"</tr>";
		if ($('tr#'+row_id).length == 0)
		{
 		$('#class_table > tbody:last-child').append(html_to_append);
		fetch_dels()
 		}	
 		
 		};

fetch_dels()
$('#add_class').on('click', function () {
 		add_class()
 	 	
 	});

$('div.hit').each(function () {

	$(this).on('click', function() {	
		$(this).children('div.bottom').slideToggle(500);
		console.log($(this).children('div.bottom'))
		})
	
	})


$('div.empty_hit').each(function () {

	$(this).on('click', function() {	
		$(this).children('div.bottom').slideToggle(500);
		console.log($(this).children('div.bottom'))
		}
	)
});

$('#str_open').on('click', function() {
	$('#ketcher_div').toggle(500);

});

$('#op_open').on('click', function() {
	$('#options_block').toggle(500);

});


$('#ketcher-frame').on('load', function () {
          var ketcher = this.contentWindow.ketcher,
              source = $('#id_smiles');
              //molecule=localStorage.getItem('molecule');
              
			 //console.log(molecule);
			 //ketcher.setMolecule(molecule);
			 //source.val(ketcher.getSmiles());
              
          $('#form_input').on('click', function () {
	   		//ketcher.onStructChange(function() {
            	source.val(ketcher.getSmiles());
            	var molecule=ketcher.getMolfile();
            	console.log(molecule);
            	localStorage.setItem('molecule',molecule);
            });
         //   }); 
      	//$('#str_open').on('click', function() {              
			//	var molecule=localStorage.getItem('molecule');
			//	console.log(molecule);
			//	ketcher.setMolecule(molecule);
			//	source.val(ketcher.getSmiles());
		//});
			
		});
		
});
