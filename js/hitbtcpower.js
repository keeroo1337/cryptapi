$(document).ready(function(){
	$.post("/cgi-bin/main.py", function( data ) {
	  	$("#content").append(data);

		$( "#main" ).css("display", "table");
		$( "#main" ).css("table-layout", "fixed");
		$( "#main" ).css("border-spacing", "0px");

		$("#main").tablesorter();

		$("#main").css("width", "300px");
		$("#main").css("display", "table-cell");

	});

});