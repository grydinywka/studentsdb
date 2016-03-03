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

String.format = function() {
    // The string containing the format items (e.g. "{0}")
    // will and always has to be the first argument.
    var theString = arguments[0];
    
    // start with the second argument (i = 1)
    for (var i = 1; i < arguments.length; i++) {
        // "gm" = RegEx options for Global search (more than one instance)
        // and for Multiline search
        var regEx = new RegExp("\\{" + (i - 1) + "\\}", "gm");
        theString = theString.replace(regEx, arguments[i]);
    }
    
    return theString;
}

function initEditStudentForm(form, modal, link) {
	var spinner = $('#spinner_job');
	var modal_job = $('#modal_job');
	// attach datepicker
	initDateFields();

	// close modal window on Cancel button click
	form.find('input[name="cancel_button"]').click(function(event){
		modal.modal('hide');
		return false;
	});

	// make form work in AJAX mode
	form.ajaxForm({
		'dataType': 'html',
		'beforeSend': function(xhr,setting){
			modal_job.modal('show');
			spinner.show();
			$('input').attr('readonly', 'readonly');
		},
		'error': function(){
			spinner.hide();
			modal_job.modal('hide');
			$('#content-colomns div').html('<div class="alert alert-warning">\
			 Error on server. Attempt later, please! </div>');
			return false;
		},
		'success': function(data, status, xhr) {
			var html = $(data), newform = html.find('#content-colomn form.a');
			var alert_my = html.find('.alert');

			spinner.hide();
			modal_job.modal('hide');

			// copy alert to modal window
			modal.find('.modal-body').html(alert_my);

			// copy form to modal if we found it in server response
			if (newform.length > 0) {
				modal.find('.modal-body').append(newform);

				//initialize form fields and buttons
				initEditStudentForm(newform, modal, link);
			} else {
				// if no form, it means success and we need to reload page
				// to get updated students list;
				// reload after 2 seconds, so that user can read
				// success message

				$('#content-colomns div').html(alert_my);
				var str = String.format('a[href="{0}"]', link.attr('href'));
				var my_stud = html.find(str).parent().parent();

				my_stud.find('li').insertAfter(my_stud.find('ul.dropdown-menu'));
				// my_stud.find('ul').append(my_stud.find('li'));
				$('#student-id-my').html(my_stud.children());

				modal.modal('hide');
				// setTimeout(function(){location.reload(true);}, 500);
			}
		}
	});
}

function initEditStudentPage() {
	$('a.student-edit-form-link').click(function(event){
		var link = $(this);
		var spinner = $('#spinner');
		link.parent().parent().attr('id', 'student-id-my');

		$.ajax({
			'url': link.attr('href'),
			'dataType': 'html',
			'type': 'get',
			'beforeSend': function(xhr,setting){
				spinner.show();
				$('a').css({"pointer-events": "none",
       						"cursor": "default"});
			},
			'success': function(data, status, xhr){
				spinner.hide();
				$('a').css({"pointer-events": "auto",
       						"cursor": "pointer"});

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

				// init our edit form
				initEditStudentForm(form, modal, link);

				// setup and show modal window finally
				modal.modal({
					'keyboard': false,
					'backdrop': false,
					'show': true
				});

			},
			'error': function(){
				spinner.hide();
				$('#content-colomns div').html('<div class="alert alert-warning">\
				 Error on server. Attempt later, please! </div>');
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
