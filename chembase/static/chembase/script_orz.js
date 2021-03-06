$(document).ready(function(){

$('div.item').each(function () {

	$(this).on('click', function() {	
		$(this).children('div.bottom').slideToggle(500);
		console.log($(this).children('div.bottom'))
		})
	
	});
	

$('#id_owner').val('')

$('#id_owner').on('change', function() {
		console.log($(this).val());
		var owner=$(this).val();
		if (owner=='') {$('#hidden_field').slideUp(500)}
		else {$('#hidden_field').slideDown(500);
		$('#id_stanowisko').val($('#id_owner option:selected').text());		
		}

})
	
$('#new_form').on('click',function () {
	$('#orz_form').slideToggle(500);

})

$('#orz_submit_form').on('submit', function(event) {
		event.preventDefault();
		var owner=$('#id_owner').val();
		var stanowisko=$('#id_stanowisko').val();
		var kod=$('#id_kod_stanowiska').val();
		var from=$('#id_date_from').val();
		var to=$('#id_date_to').val();
		$('#orz_input').hide();
		$('#wait_box').show();
		
		send_orz(owner,stanowisko,kod,from,to);
		console.log('submitted');
		
	});


function send_orz(owner,stanowisko,kod,from,to) {
		console.log('finding started');
		$.ajax({
			url :'/admin/orz',
			type : "POST",
			data : {'owner': owner,'date_from':from,'date_to':to,'stanowisko':stanowisko,'kod_stanowiska':kod},
			
			success : function(json) {
				console.log(json);
				console.log('success');
				
				var html_div="<div class='item' id="+json['code']+">"+
				"<div class='top'>"+
				"<div class='code'>"+json['code']+"</div>"+
				"<div class='opis'>Group:</div>"+
				"<div class='val_long'>"+json['owner']+"</div>"+
				"<div class='opis'>From:</div>"+
				"<div class='val'>"+json['from']+"</div>"+
				"<div class='opis'>To:</div>"+
				"<div class='val'>"+json['to']+"</div>"+
				"<div class='opis'>Author:</div>"+
				"<div class='val'>"+json['author']+"</div>"+
				"<div class='pdf'><a target='_blank' href='{% static '/chembase/data/orz/' %}"+json['code']+"/ORZaII.pdf'>PDF</a></div>"+
				"</div>"+
				"<div class='bottom' style='display:block'>"+
				"<div class='opis'>Created:</div>"+
				"<div class='val'>"+json['created']+"</div>"+
				"<div class='opis' id='incl_cmpds'>Included compounds:</div>"+
				"<div class='val'>"+json['num']+"</div>"+
				"<div class='opis'>Status:</div>"+
				"<div class='val'>"+json['status']+"</div></div></div>"
				console.log(html_div)
				$('#entries').prepend(html_div);
				$('#wait_box').fadeOut('fasf',function(){$('#orz_input').fadeIn('fast')});
	


					},		
				
			error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText);
            var error_p="<p class='warning'> From not created - system error. Server response: "+xhr.status + ": " + xhr.responseText+"</p>"
            $('#wait_box').fadeOut('fasf',function(){$('#orz_input').fadeIn('fast')});
            $('#entries').prepend(error_p);
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