$(document).ready(function(){
	
	
	$('#cas_form').on('submit', function(event) {
		event.preventDefault();
		console.log($('#id_query').val());
		find_cas();	
		
	});

	
	function find_cas() {
		console.log('finding started');
		$.ajax({
			url :'/search_ajax/',
			type : "POST",
			data : {query : $('#id_query').val(),cutoff:0.5},
			
			success : function(json) {
				console.log(json);
				console.log('success');
				$.each(json, function(index,obj) {  
					console.log(index);
					console.log(obj['subtitle']);
					var html_res='<tr>' +
					 "<td><img class='structure' src='/static/chembase/"+obj['image']+"' alt='structure'/></td>" +
					 '<td>'+obj['name']+'</td>' + 
					 '<td>'+obj['subtitle']+'</td>' +
					 '<td>'+obj['cas']+'</td>' +
					 '<td><input type="button" name="'+index+'" value="Choose" /></td>'+
					 '</tr>'
					$('#results tbody').append(html_res);
					//$('#first_box').animate({left:'-5000px'},'fasf',function(){$('#first_box').hide()});
					//$('#second_box').show('fasf',function(){$('#second_box').animate({left:'0px'},'fast')});
					//$('#second_box').show('fasf',function(){$('#second_box').animate({left:'0px'},'fast')});
					console.log(html_res);
					
					});
				$('#first_box').fadeOut('fasf',function(){$('#second_box').fadeIn('fast')});
				$('#results').find('input').each(function() {
					$(this).on('click', function() {
							var cmpd_id=$(this).attr('name');
							console.log(cmpd_id);
							$('#id_field').attr('value',cmpd_id);
							$('#type_field_3').attr('value','base');
							$('#hidden_form').submit();
					});		
				
					});
				},
				
			error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText)
            
            }
				
			
		});
		
		
	};
	
	
	$('#back_input').on('click',function (){
		$('#second_box').fadeOut('fasf',function(){$('#first_box').fadeIn('fast',function() {$('#results tbody > tr').remove()})});
	
	});
	
	$('#back_chemspi').on('click',function (){
		$('#third_box').fadeOut('fasf',function(){$('#second_box').fadeIn('fast',function() {$('#results_spider tbody > tr').remove()})});
	
	});
	
	$('#chemspider_input').on('click',function () {
			console.log('started chemspider');
			console.log($('#id_query').val());
			$('#second_box').fadeOut('fasf',function(){$('#hide').fadeIn('fast')});
			find_chemspy();
		
	});
	
	
	
	function find_chemspy() {
		console.log('finding started');
		$.ajax({
			url :'/search_ajax_chemspy/',
			type : "POST",
			data : {query : $('#id_query').val()},
			
			success : function(json) {
				console.log(json);
				console.log('success');
				$.each(json, function(index,obj) {  
					console.log(index);
					var html_res='<tr>' +
					 "<td><img class='structure' src="+obj['image']+" alt='structure'/></td>" +
					 '<td>'+obj['name']+'</td>' + 
					 '<td>'+obj['iupac_name']+'</td>' +
					 '<td>'+obj['cas']+'</td>' +
					 '<td>'+obj['csid']+'</td>' +
					 '<td>'+obj['formula']+'</td>' +
					 '<td><input type="button" name="'+index+'" num="'+obj['cas']+'" value="Choose" /></td>'+
					 '</tr>'
					$('#results_spider tbody').append(html_res);
					//$('#first_box').animate({left:'-5000px'},'fasf',function(){$('#first_box').hide()});
					//$('#second_box').show('fasf',function(){$('#second_box').animate({left:'0px'},'fast')});
					//$('#first_box').fadeOut('fasf',function(){$('#second_box').fadeIn('fast')});
					//$('#second_box').show('fasf',function(){$('#second_box').animate({left:'0px'},'fast')});
					console.log(html_res);
					
					});
					$('#hide').fadeOut('fasf',function(){$('#third_box').fadeIn('fast')});
					$('#results_spider').find('input').each(function() {
					$(this).on('click', function() {
							var cmpd_id=$(this).attr('name');
							var cas=$(this).attr('num');
							console.log(cmpd_id);
							$('#id_field').attr('value',cmpd_id);
							$('#cas_field').attr('value',cas);
							$('#type_field_3').attr('value','spider');
							$('#hidden_form').submit();
					});		
				
					});
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
