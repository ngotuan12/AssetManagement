/**
 * @author: TuanNA
 * @since: 11/09/2014
 * @version: 1.0 Copyright 2014, Ngo Anh Tuan
 */
(function($)
{
	
	
	$.fn.loading = {
		show: function()
		{
			$('body').css("overflow","auto");
			$.loading.loadMask();
			//addloading
			loading = $('<div id="status"><i class="fa fa-spinner fa-spin"></i></div>');
			loading.appendTo('body');

		},
		hide: function()
		{
			jQuery('#status').fadeOut(function()
			{
				jQuery('body #status').remove();
				jQuery('#background-mask').remove();
			});
		},
	};
	var mask, size, loading;
	
	$.loading = {
		loadMask: function()
		{
			mask = $('<div id="background-mask" />').appendTo($('body'));
			mask.css({
				position : 'fixed',
				top : 0,
				left : 0,
				width : '100%',
				height : '100%',
				display : 'none',
				opacity : 0,
				zIndex : 9999,
				backgroundColor : '#000'
			});

			mask.css({
				display : 'block'
			}).fadeTo('400', 0);

		},
	};
})(jQuery);
