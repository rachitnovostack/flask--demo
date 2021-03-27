"use strict";

// Shared Colors Definition
const primary = '#6993FF';
const success = '#1BC5BD';
const info = '#8950FC';
const warning = '#FFA800';
const danger = '#F64E60';


var KTApexChartsDemo = function () {

	var _demo3 = function () {
		const apexChart = "#chart_3";
		var options = {
			series: [{
				name: 'Incoming',
				data: [44, 55, 57, 56, 61, 58, 63, 60, 66]
			}, {
				name: 'Outgoing',
				data: [35, 41, 36, 26, 45, 48, 52, 53, 41]
			}],
			chart: {
				type: 'bar',
				height: 350
			},
			plotOptions: {
				bar: {
					horizontal: false,
					columnWidth: '55%',
					endingShape: 'rounded'
				},
			},
			dataLabels: {
				enabled: false
			},
			stroke: {
				show: true,
				width: 2,
				colors: ['transparent']
			},
			xaxis: {
				categories: ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'],
			},
			yaxis: {
				title: {
					text: '$ (thousands)'
				}
			},
			fill: {
				opacity: 1
			},
			tooltip: {
				y: {
					formatter: function (val) {
						return "$ " + val + " thousands"
					}
				}
			},
			colors: [primary, warning]
		};

		var chart = new ApexCharts(document.querySelector(apexChart), options);
		chart.render();
	}

	var _demo4 = function () {
		const apexChart = "#chart_4";
		var options = {
			series: [{
				name: 'Incoming',
				data: [44, 55, 57, 56, 61, 58, 63, 60, 66]
			}, {
				name: 'Outgoing',
				data: [35, 41, 36, 26, 45, 48, 52, 53, 41]
			}],
			chart: {
				type: 'bar',
				height: 350
			},
			plotOptions: {
				bar: {
					horizontal: false,
					columnWidth: '55%',
					endingShape: 'rounded'
				},
			},
			dataLabels: {
				enabled: false
			},
			stroke: {
				show: true,
				width: 2,
				colors: ['transparent']
			},
			xaxis: {
				categories: ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'],
			},
			yaxis: {
				title: {
					text: '$ (thousands)'
				}
			},
			fill: {
				opacity: 1
			},
			tooltip: {
				y: {
					formatter: function (val) {
						return "$ " + val + " thousands"
					}
				}
			},
			colors: [primary, warning]
		};

		var chart = new ApexCharts(document.querySelector(apexChart), options);
		chart.render();
	}

	var _demo12 = function () {
		const apexChart = "#chart_12";
		var options = {
			series: [44, 55, 33, 38],
			chart: {
				width: 380,
				type: 'pie',
			},
			labels: ['Error 404', 'Error 408', 'Error 304', 'Error 400'],
			responsive: [{
				breakpoint: 480,
				options: {
					chart: {
						width: 200
					},
					legend: {
						position: 'bottom'
					}
				}
			}],
			colors: [primary, success, warning, danger]
		};

		var chart = new ApexCharts(document.querySelector(apexChart), options);
		chart.render();
	}

	var _demo13 = function () {
		const apexChart = "#chart_13";
		var options = {
			series: [44, 55, 33, 38],
			chart: {
				width: 380,
				type: 'pie',
			},
			labels: ['Error 404', 'Error 408', 'Error 304', 'Error 400'],
			responsive: [{
				breakpoint: 480,
				options: {
					chart: {
						width: 200
					},
					legend: {
						position: 'bottom'
					}
				}
			}],
			colors: [primary, success, warning, danger]
		};

		var chart = new ApexCharts(document.querySelector(apexChart), options);
		chart.render();
	}

	return {
		// public functions
		init: function () {
			_demo3();
			_demo4();
			_demo12();
			_demo13();
		}
	};
}();

jQuery(document).ready(function () {
	KTApexChartsDemo.init();
});


$(document).ready(function () {
	// Begin: show / hide password
  	$("body").on('click','.toggle-password',function(){
	    $(this).toggleClass("fa-eye fa-eye-slash");

	    var input = $(this).parent().find("#pass_log_id");

	    if (input.attr("type") === "password") {
	        input.attr("type", "text");
	    } else {
	        input.attr("type", "password");
	    }
	});
	// End: Show / Hide Password

	// Begin: search / filter table
	$('.dataTables').DataTable();
	// End: search / filter table

	// Begin: daterange picker
	$('.daterange').daterangepicker({
		maxDate: new Date(),
		locale: {
            format: 'DD/MMM/YYYY'
        }
	});
	$('.daterange1').daterangepicker({
		maxDate: new Date(),
		locale: {
            format: 'DD/MMM/YYYY'
        }
	});
	// End: daterange picker

	$(".formFields").hide();

	// Begin: show / Hide fields, if NEEMO is selected
	$(function () {
	  	$("#select_plat").change(function() {
	    	var val = $(this).val();
	    	if(val === "Neemo") {
	        	$(".formFields").show();
	    	}
	    	else if(val === "Goomer") {
	        	$(".formFields").show();
	        	$(".formFields1").hide();
	    	}
	    	else if(val === "Justo") {
	        	$(".formFields").hide();
	    	}
	  	});
	});
	// End: show / Hide fields, if NEEMO is selected

	// Begin: show / Hide fields, if GOOMER is selected
	// $(function () {
	//   	$("#select_plat").change(function() {
	//     	var val = $(this).val();
	//     	if(val === "Goomer") {
	//         	$(".formFields1").show();
	//     	}
	//     	else {
	//         	$(".formFields").hide();
	//     	}
	//   	});
	// });
	// End: show / Hide fields, if GOOMER is selected
});