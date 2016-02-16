var my_json = $.ajax({
	url: '/journal2/',
	type: 'get',
	dataType: 'json',

	success: function(){
		alert('Load was performed!');
	}
});

document.write(<p></p> + my_json);
