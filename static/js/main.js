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
				$('div#presence_error').append(gettext("<p>" + error + "</p>"));
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

function getCurrPage(link, str) {
	var html;
	$.ajax({
		'url': window.location.href,
		'dataType': 'html',
		'type': 'get',
		'beforeSend': function(xhr,setting){
			html = '<h1>beforeSend</h1>';
		},
		'success': function(data, status, xhr){
			if (status != 'success') {
				alert(gettext('Error on server. Attempt later, please!'));
				return false;
			}
			html = $(data);
			if ( link.is('.add_stud, .group-add-form-link') ) {
				$('tbody').html(html.find('tbody tr'));
			} else if ( link.is('a.student-edit-form-link, a.group-edit-form-link') ) {
				var my_stud = html.find(str).parent().parent();
				link.parent().parent().html(my_stud.find('td'));
			}
			initEditAddStudentPage();
			initEditGroupPage();
		},
		'error': function(){
			html = gettext('<h1>Error</h1>');
		}
	});

	return false;
}

function initEditAddStudentForm(form, modal, link) {
	var spinner = $('#spinner_job');
	var modal_job = $('#modal_job');
	// attach datepicker
	initDateFields();

	// close modal window on Cancel button click
	form.find('input[name="cancel_button"]').click(function(event){
		modal.modal('hide');
		var html = $(data);
		var alert_my = html.find('.alert');
		// $('#content-colomns div').html(alert_my);
		return false;
	});

	// make form work in AJAX mode
	form.ajaxForm({
		'dataType': 'html',
		'beforeSend': function(xhr,setting){
			modal_job.modal('show');
			spinner.show();
			$('input, select').attr('readonly', 'readonly');
			$('input, select').attr('disabled', 'disabled');
		},
		'error': function(){
			spinner.hide();
			modal_job.modal('hide');
			$('#content-colomns div').html(gettext('<div class="alert alert-warning">\
						 Error on server. Attempt later, please! </div>'));

			return false;
		},
		'success': function(data, status, xhr) {
			var html = $(data), newform = html.find('#content-colomn form.a');
			var alert_my = html.find('.alert');

			spinner.hide();
			modal_job.modal('hide');
			$('input, select').attr('readonly', false);
			$('input, select').attr('disabled', false);

			// copy alert to modal window
			modal.find('.modal-body').html(alert_my);

			// copy form to modal if we found it in server response
			if (newform.length > 0) {
				modal.find('.modal-body').append(newform);

				//initialize form fields and buttons
				initEditAddStudentForm(newform, modal, link);
			} else {
				// if no form, it means success and we need to reload page
				// to get updated students list;
				// reload after 2 seconds, so that user can read
				// success message

				$('#content-colomns div').html(alert_my);

				var str = String.format('a[href="{0}"]', link.attr('href'));
				html = getCurrPage(link, str);
				

				modal.modal('hide');
				// setTimeout(function(){location.reload(true);}, 500);
				
			}
		}
	});
}

function initEditAddStudentPage() {
	$('a.student-edit-form-link, a.add_stud').click(function(event){
		var link = $(this);
		var spinner = $('#spinner');

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
					alert(gettext('Error on server. Attempt later, please!'));
					return false;
				}
				// update modal window with arrived content from the server
				var modal = $('#myModal'),
					html = $(data),
					form = html.find('#content-colomn form');

				modal.find('.modal-title').html(html.find('#content-column h2').text());
				modal.find('.modal-body').html(form);

				// init our edit form
				initEditAddStudentForm(form, modal, link);

				// setup and show modal window finally\
				modal.modal({
					'keyboard': false,
					'backdrop': false,
					'show': true
				});
			},
			'error': function(){
				spinner.hide();
				modal.modal('hide');
				$('a').css({"pointer-events": "auto",
       						"cursor": "pointer"});
				$('#content-colomns div').html(gettext('<div class="alert alert-warning">\
								 Error on server. Attempt later, please! </div>'));
				alert(gettext('There was an error on the server!'));
				return false;
			}
		});
		event.preventDefault();
		return false;
	});
}

function initDelete_multStudentForm() {
	var form = $('form#delete_mult'),
		modal = $('#myModal');
	var spinner = $('#spinner');

	// post from main page
	form.ajaxForm({
		'dataType': 'html',
		'beforeSend': function(xhr, setting){
			spinner.show();
			$('a').css({"pointer-events": "none",
       						"cursor": "default"});
			$('input').attr('disabled', true);
		},
		'success': function(data, status, xhr) {
			var html = $(data);
			var newform = html.find('form');

			spinner.hide();
			$('a').css({"pointer-events": "auto",
   						"cursor": "pointer"});
			$('input').attr('disabled', false);

			modal.find('.modal-title').html(html.find('#content-column h2').text());
			if (newform.length == 1) {
				var spinner_job = $('#spinner_job');
				var modal_job = $('#modal_job');

				modal.find('.modal-body').html(newform);

				// post from modal window delete_mult
				newform.ajaxForm({
					'dataType': 'html',
					'beforeSend': function(xhr2, setting2){
						$('input').attr('disabled', true);
						modal_job.modal('show');
						spinner_job.show();
					},
					'success': function(data2, status2, xhr2){
						var html2 = $(data2);
						var alert_my = html2.find('.alert');

						$('#content-colomns div').html(alert_my);
						modal.modal('hide');
						$('input').attr('disabled', false);
						modal_job.modal('hide');
						spinner_job.hide();

						$('tbody').html(html2.find('tbody tr'));
					},
					'error': function(){
						modal.modal('hide');
						$('input').attr('disabled', false);
						modal_job.modal('hide');
						spinner_job.hide();

						alert(gettext('Error on server!'));
					}
				});
			} else {
				modal.find('.modal-body').html(html.find('p#neither_stud'));
			}
			
			modal.modal('show');
		},
		'error': function(){
			spinner.hide();
			modal.modal('hide');
			$('a').css({"pointer-events": "auto",
   						"cursor": "pointer"});
			$('#content-colomns div').html(gettext('<div class="alert alert-warning">\
						 Error on server. Attempt later, please! </div>'));

			return false;
		}
	});
}

function initDeleteStudentForm(form, modal, link){
	var spinner_job = $('#spinner_job');
	var modal_job = $('#modal_job');

	form.find('input[name="cancel_button"]').click(function(event){
		modal.modal('hide');
		var html = $(data);
		var alert_my = html.find('.alert');
		return false;
	});

	form.ajaxForm({
		'dataType': 'html',
		'beforeSend': function(xhr,setting){
			modal_job.modal('show');
			spinner_job.show();
			$('input, select').attr('readonly', 'readonly');
			$('input, select').attr('disabled', 'disabled');
		},
		'error': function(){
			spinner_job.hide();
			modal_job.modal('hide');
			modal.modal('hide');
			$('input, select').attr('readonly', false);
			$('input, select').attr('disabled', false);
			$('#content-colomns div').html(gettext('<div class="alert alert-warning">\
						 Error on server. Attempt later, please! </div>'));
			return false;
		},
		'success': function(data, status, xhr) {
			var html = $(data);
			var alert_my = html.find('.alert');

			spinner_job.hide();
			modal_job.modal('hide');
			$('input, select').attr('readonly', false);
			$('input, select').attr('disabled', false);

			// copy form to modal if we found it in server response
			
			// if no form, it means success and we need to reload page
			// to get updated students list;
			// reload after 2 seconds, so that user can read
			// success message

			$('#content-colomns div').html(alert_my);
			link.closest('tr').remove();
			
			modal.modal('hide');
		}
	});
}

function initDeleteStudentPage() {
	$('a.student-delete-form-link, a.group-delete-form-link').click(function(event){
		var link = $(this);
		var spinner = $('#spinner');

		$.ajax({
			'url': link.attr('href'),
			'dataType': 'html',
			'type': 'get',
			'success': function(data, status, xhr){
				if (status != 'success') {
					alert(gettext('Error on server. Attempt later, please!'));
					return false;
				}
				// update modal window with arrived content from the server
				var modal = $('#myModal'),
					html = $(data),
					form = html.find('#content-colomn form');

				modal.find('.modal-title').html(html.find('#content-column h2').text());
				modal.find('.modal-body').html(form);

				// init our edit form
				initDeleteStudentForm(form, modal, link);

				// setup and show modal window finally\
				modal.modal({
					'keyboard': false,
					'backdrop': false,
					'show': true
				});
			}
		});
	
		return false;
	});
}

function initEditGroupForm(form, modal, link) {
	var spinner_job = $('#spinner_job');
	var modal_job = $('#modal_job');

	form.find('input[name="cancel_button"]').click(function(event){
		modal.modal('hide');
		return false;
	});

	// make form work in AJAX mode.
	form.ajaxForm({
		'dataType': 'html',
		'beforeSend': function(xhr,setting){
			modal_job.modal('show');
			spinner_job.show();
			$('input, select').attr('readonly', 'readonly');
			$('input, select').attr('disabled', 'disabled');
		},
		'error': function(){
			spinner_job.hide();
			modal_job.modal('hide');
			$('#content-colomns div').html(gettext('<div class="alert alert-warning">\
						 Error on server. Attempt later, please! </div>'));
			return false;
		},
		'success': function(data, status, xhr) {
			var html = $(data), newform = html.find('#content-colomn form');
			var alert_my = html.find('.alert');

			spinner_job.hide();
			modal_job.modal('hide');

			// copy alert to modal window
			modal.find('.modal-body').html(alert_my);

			if (newform.length > 0) {
				modal.find('.modal-body').append(newform);

				//initialize form fields and buttons
				initEditGroupForm(newform, modal, link);
			} else {
				$('#content-colomns div').html(alert_my);

				var str = String.format('a[href="{0}"]', link.attr('href'));
				html = getCurrPage(link, str);

				modal.modal('hide');
			}
		}
	});

}

function initEditGroupPage() {
	$('.group-edit-form-link, .group-add-form-link').click(function(event){
		var link = $(this),
			spinner = $('#spinner');

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
					alert(gettext('Error on server. Attempt later, please!'));
					return false;
				}
				// update modal window with arrived content from the server
				var modal = $('#myModal'),
					html = $(data),
					form = html.find('#content-colomn form');

				modal.find('.modal-title').html(html.find('#content-column h2').text());
				modal.find('.modal-body').html(form);

				initEditGroupForm(form, modal, link);

				modal.modal({
					'keyboard': false,
					'backdrop': false,
					'show': true
				});

			},
			'error': function(){
				spinner.hide();
				$('a').css({"pointer-events": "auto",
       						"cursor": "pointer"});
				$('#content-colomns div').html(gettext('<div class="alert alert-warning">\
								 Error on server. Attempt later, please! </div>'));

				return false;
			}
		});
		
		return false;
	});
}

function initEditJournalPage() {
	$("a.student-journal-form-link, a.group-journal-form-link").click(function(event){
		var link = $(this),
			spinner = $('#spinner');

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
					alert(gettext('Error on server. Attempt later, please!'));
					return false;
				}
				// update modal window with arrived content from the server
				var modal = $('#myModal'),
					html = $(data),
					table = html.find('#content-colomn');

				modal.find('.modal-dialog').css({'width': '1100px'});

				modal.find('.modal-title').html(html.find('#content-column h2').text());
				modal.find('.modal-body').html(table);

				modal.modal({
					'keyboard': false,
					'backdrop': false,
					'show': true
				});
			},
			'error': function(){
				spinner.hide();
				modal.modal('hide');
				$('a').css({"pointer-events": "auto",
       						"cursor": "pointer"});
				$('#content-colomns div').html(gettext('<div class="alert alert-warning">\
								 Error on server. Attempt later, please! </div>'));

				return false;
			}
		});
		
		return false;
	});
}

function initTabs() {
	var navLinks = $('li a.tab');
	navLinks.click(function(event){
		var link = $(this), spinner = $('#spinner');

		$.ajax({
			'url': link.attr('href'),
			'dataType': 'html',
			'type': 'get',
			'beforeSend': function(xhr,setting){
				spinner.show();
				$('a').css({"pointer-events": "none",
							"cursor": "default"});
				$('input, select').attr('disabled', 'disabled');
			
			},
			'success': function(data, status, xhr){
				spinner.hide();
				$('a').css({"pointer-events": "auto",
       						"cursor": "pointer"});
				$('input, select').attr('disabled', false);

				// check if we got successfull response from the server
				if (status != 'success') {
					alert(gettext('Error on server. Attempt later, please!'));
					return false;
				}
				// update modal window with arrived content from the server
				var body = $('#content-colomn'),
					html = $(data);
				var pageTitle = html.find('h2').text();

				body.html(html.find('#content-colomn div.col-xs-12'));
				$('#content-column').parent().html(html.find('#content-column').parent().children());
				$('.alert').remove();
				navLinks.each(function(index){
					if ($(this).attr('href') === link.attr('href')) {
						$(this).parent().addClass('active');
					} else {
						$(this).parent().removeClass('active');
					}
				});

				window.history.pushState("string", pageTitle, link.attr('href'));
				document.title = html.filter('title').text();

				initJournal();
				initGroupSelector();
				initDateFields();
				initEditAddStudentPage();
				initEditGroupPage();
				initDelete_multStudentForm();
				initDeleteStudentPage();
				initEditJournalPage();
				// initTabs();
				initSort();
				initPagination();
			},
			'error': function(){
				spinner.hide();
				$('a').css({"pointer-events": "auto",
       						"cursor": "pointer"});
				$('input, select').attr('disabled', false);
				$('#content-colomns div').html(gettext('<div class="alert alert-warning">\
								 Error on server. Attempt later, please! </div>'));

				return false;
			}
		});

		return false;
	});
}

function initSort(){
	var sortLink = $('tr th > a'), spinner = $('#spinner');

	sortLink.click(function(event){
		var link = $(this);

		$.ajax({
			'url': link.attr('href'),
			'dataType': 'html',
			'type': 'get',
			'beforeSend': function(xhr,setting){
				spinner.show();
				$('a').css({"pointer-events": "none",
							"cursor": "default"});
				$('input, select').attr('disabled', 'disabled');
			
			},
			'success': function(data, status, xhr){
				spinner.hide();
				$('a').css({"pointer-events": "auto",
       						"cursor": "pointer"});
				$('input, select').attr('disabled', false);

				// check if we got successfull response from the server
				if (status != 'success') {
					alert(gettext('Error on server. Attempt later, please!'));
					return false;
				}

				var html = $(data);
				$('.table').html(html.find('.table'));
				window.history.pushState("string", "pageTitle", link.attr('href'));
				initJournal();
				initGroupSelector();
				initDateFields();
				initEditAddStudentPage();
				initEditGroupPage();
				initDelete_multStudentForm();
				initDeleteStudentPage();
				initEditJournalPage();
				initTabs();
				// initSort();
				initPagination();
			},
			'error': function(){
				spinner.hide();
				$('a').css({"pointer-events": "auto",
       						"cursor": "pointer"});
				$('input, select').attr('disabled', false);
				$('#content-colomns div').html(gettext('<div class="alert alert-warning">\
								 Error on server. Attempt later, please! </div>'));

				return false;
			}
		});

		return false;
	});
}

function initPagination() {
	var pageLink = $('ul.pagination li a');

	pageLink.click(function(event){
		var link = $(this);

		$('.alert-warning').hide();
		$.ajax({
			'url': link.attr('href'),
			'dataType': 'html',
			'type': 'get',
			'success': function(data, status, xhr){
				var html = $(data);

				$('.table').html(html.find('.table'));
				window.history.pushState("string", "pageTitle", link.attr('href'));
				pageLink.each(function(index){
					if ($(this).attr('href') === link.attr('href')) {
						if (index === 0) {
							$(this).parent().next().addClass("active");
						} else if (index === (pageLink.length - 1)) {
							$(this).parent().prev().addClass("active");
						} else {
							$(this).parent().addClass("active");
						}
					} else {
						$(this).parent().removeClass("active");
					}
				});
			initJournal();
			initGroupSelector();
			initDateFields();
			initEditAddStudentPage();
			initEditGroupPage();
			initDelete_multStudentForm();
			initDeleteStudentPage();
			initEditJournalPage();
			initTabs();
			initSort();
			}
		});

		return false;
	});
}

function loadMoreStudents() {
	$('#load_more').click(function () {
		// var page_num = parseInt($(this).data('page'), 10);
		var $this = $(this);
		var num_page = parseInt($this.data('num-pages'), 10);
		var page_number = parseInt($this.data('page'), 10) + 1;
		var url_to_go = ("/?page=").concat(page_number);
		$('#navigation').hide();
		$('#loading').show();

		$.ajax({
			url: url_to_go,
			dataType: 'html',
			success: function(html) {
				var html = $(html);
				var rows = html.find('tbody').children();

				$('tbody').append(rows);
				$('#loading').hide();
				$this.data("page", page_number);
				if ( page_number == num_page ) {
					$this.hide();
				}

				// alert($this.text());
				// alert($this.data("page"));
			}
		});
	});
}


function infinityScroll() {
	var win = $(window);
	var sign_end = false;
	var $l_m = $('#load_more');
	$('#navigation').hide();
	
	$(window).endlessScroll({
		inflowPixels: 300,
		callback: function() {
			// if it is not all students
			if ( sign_end == false ) {
				var num_page = parseInt($l_m.data('num-pages'), 10);
				var page_number = parseInt($l_m.data('page'), 10) + 1;
				var url_to_go = ("/?page=").concat(page_number);
				$('#loading').show();

				$.ajax({
					url: url_to_go,
					dataType: 'html',
					success: function(html) {
						var html = $(html);
						var rows = html.find('tbody').children();

						$l_m.data("page", page_number);
						$('tbody').append(rows);
						$('#loading').hide();
						if ( page_number >= num_page ) {
							$l_m.hide();
							sign_end = true;
						}
					}
				});
			}
		}
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

function setLanguage() {
	$('.lang').click(function(event){
		var lang = $(this);
		$.ajax(lang.data('url'), {
			'type': 'GET',
			'async': true,
			'dataType': 'json',
			'beforeSend': function(xhr,setting){
				
			},
			'error': function(xhr, status, error){
				$('#content-colomns div').html(gettext('<div class="alert alert-warning">\
						 Error on server. Attempt later, please! </div>'));
			},
			'success': function(data, status, xhr){
				$.cookie(data.django_lang, lang.attr('value') , {'path': '/', 'expires': 365});
				
				$('#content-colomns div').html(gettext('<div class="alert alert-success">\
						 Language set! </div>'));
				location.reload(true);
			}
		});
		
		// and reload a page
		

		return true;
	});
}

$(document).ready(initFunction);

function initFunction(){
	initJournal();
	initGroupSelector();
	initDateFields();
	initEditAddStudentPage();
	initEditGroupPage();
	initDelete_multStudentForm();
	initDeleteStudentPage();
	initEditJournalPage();
	initTabs();
	initSort();
	initPagination();
	setLanguage();

	loadMoreStudents();
	infinityScroll();
}