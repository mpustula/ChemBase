$(document).ready(function() {

	$('div.experiment').each(function () {

		$(this).on('click', function () {
			$(this).children('div.hidden').slideToggle(500);
			console.log($(this).children('div.hidden'))
		})

	})

})
