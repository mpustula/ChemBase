
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
              mol=$('#id_molecule');


			ketcher.onStructChange(function() {
            source.val(ketcher.getSmiles());
            });

});

});