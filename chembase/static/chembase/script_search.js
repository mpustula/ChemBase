
$(document).ready(function(){


$('div.hit').each(function () {

	$(this).on('click', function() {	
		$(this).children('div.bottom').slideToggle(500);
		console.log($(this).children('div.bottom'))
		}
	)
});

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
            	//console.log(molecule);
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
