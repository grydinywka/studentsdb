function initJournal() {
	var indicator = $('#ajax-progress-indicator');
	var presence_error = $('#presence_error');

	$('.day-box input[type="checkbox"]').click(function(event){
		var box = $(this);
		$.ajax(box.data('url'), {
			'type': 'POST',
			'async': true,
			'dataType': 'json',
			'data': {
				'pk': box.data('student-id'),
				'date': box.data('date'),
				'present': box.is(':checked') ? '1': '',
				'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
			},
			'beforeSend': function(xhr,setting){
				indicator.show();
				// presence_error.hide();
			},
			'error': function(xhr, status, error){
				// alert(error);
				indicator.hide();
				presence_error.show();
				$('div#presence_error').append("<p>" + error + "</p>");
			},
			'success': function(data, status, xhr){
				indicator.hide();
				presence_error.hide();
			}
		});
	});
}

$(document).ready(function(){
	initJournal();
});