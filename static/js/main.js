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

function initGroupSelector() {
	// look up select element with groups and attach our even handler 
	// on field "change" event
	$('#group-selector select').change(function(event){
		// get value of currently selected group option
		var group = $(this).val();

		if (group) {
			// set cookie with expiration date 1 year since now;
			// cookie creation function takes period in days
			$.cookie('current_group', group, {'path': '/', 'expires': 365});
		} else {
			// otherwise we delete the cookie
			$.removeCookie('current_group', {'path': '/'});
		}

		// and reload a page
		location.reload(true);

		return true;
	});
}

function initDateFields() {
	var inp = 'input.dateinput';
	var inpExam = 'input.datetimeinput';

	if ($(inp).length > 0) {
		$(inp).wrap('<div class="input-group date col-sm-4"></div>');
		$('<span class="input-group-addon">\
			 <span class="glyphicon glyphicon-calendar"></span>\
		   </span>').insertAfter(inp);
		$('.date').datetimepicker({
			format: 'YYYY-MM-DD',
			locale: 'uk'
		}).on('dp.hide', function(event){
			$(this).blur();
		});
	} else if ($(inpExam).length > 0) {
		$(inpExam).wrap('<div class="input-group date col-sm-4"></div>');
	
		$('<span class="input-group-addon">\
			 <span class="glyphicon glyphicon-calendar"></span>\
		   </span>').insertAfter(inpExam);
		$(inpExam).datetimepicker({
			format: 'YYYY-MM-DD HH:mm',
			locale: 'uk'
		}).on('dp.hide', function(event){
			$(this).blur();
		});
	}
}

function initEditStudentPage() {
	$('a.student-edit-form-link').click(function(event){
		var link = $(this);
		$.ajax({
			'url': link.attr('href'),
			'dataType': 'html',
			'type': 'get',
			'success': function(data, status, xhr){
				// check if we got successfull response from the server
				if (status != 'success') {
					alert('Error on server. Attempt later, please!');
					return false;
				}
				// update modal window with arrived content from the server
				var modal = $('#myModal'),
					html = $(data),
					form = html.find('#content-colomn form');
				modal.find('.modal-title').html(html.find('#content-column h2').text());
				modal.find('.modal-body').html(form);

				// setup and show modal window finally
				modal.modal('show');
			},
			'error': function(){
				alert('Error on server, Attempt later, please!');
				return false;
			}
		});

		return false;
	});
}

function loadDoc() {
  var xhttp;
  if (window.XMLHttpRequest) {
    // code for modern browsers
    xhttp = new XMLHttpRequest();
    } else {
    // code for IE6, IE5
    xhttp = new ActiveXObject("Microsoft.XMLHTTP");
  }
  xhttp.onreadystatechange = function() {
    if (xhttp.readyState == 4 && xhttp.status == 200) {
      document.getElementById("demo").innerHTML = xhttp.responseText;
    }
  };
  
  xhttp.open("GET", "http://127.0.0.1:8000/static/ajax_info.txt", true);
  
  xhttp.send();
}

function canvas() {
	rect(100,50,50,50);
}

$(document).ready(function(){
	initJournal();
	initGroupSelector();
	initDateFields();
	initEditStudentPage();
});
