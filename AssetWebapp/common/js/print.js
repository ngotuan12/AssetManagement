/*
 * @author: TuanNA
 * @since: 11/09/2014
 * @version: 1.0
 * Copyright 2014, Ngo Anh Tuan
 */

(function($)
{
	var mask, size, print_modal, print_controls;
	var print_src = "";
	var print_frame_ref;
	$.fn.printPreview = function()
	{
		this.each(function()
		{
			$(this).bind('click', function(e)
			{
				e.preventDefault();
				if (!$('#print-modal').length)
				{
					print_src = $(this).attr("print-src");
					$.printPreview.loadPrintPreview();
				}
			});
		});
		return this;
	};

	$.printPreview = {
		loadPrintPreview : function()
		{
			// init
			print_modal = $('<div id="print-modal"></div>').hide();
			// print control
			print_controls = $(
					'<div id="print-modal-controls">'
							+ '<a href="#" class="print" title="Print page">Print page</a>'
							+ '<a href="#" class="close" title="Close print preview">Close</a>'
							+ '</div>');
			print_modal.append(print_controls);
			// print frame
			print_frame = $('<iframe id="print-modal-content" name="print-modal-content" scrolling="no" border="0" frameborder="0" style="overflow:hidden;overflow-x:hidden;overflow-y:hidden;height:150%;width:100%;position:absolute;top:0px;left:0px;right:0px;bottom:0px" height="150%" width="100%"> </iframe>');
			print_frame.attr("src", print_src);
			print_modal.append(print_frame);
			// add to body
			print_modal.appendTo('body');
			// The frame lives
			for (var i = 0; i < window.frames.length; i++)
			{
				if (window.frames[i].name == "print-modal-content")
				{
					print_frame_ref = window.frames[i].document;
					break;
				}
			}
			var $iframe_head = $(
					'head link[media*=print], head link[media=all]').clone();
			$iframe_head.each(function()
			{
				$(this).attr('media', 'all');
			});
			if (!$.browser.msie && !($.browser.version < 7))
			{
				$('head', print_frame_ref).append($iframe_head);
			} else
			{
				$('head link[media*=print], head link[media=all]')
						.each(
								function()
								{
									$('head', print_frame_ref)
											.append(
													$(this).clone().attr(
															'media', 'all')[0].outerHTML);
								});
			}
			// Disable all links
			$('a', print_frame_ref).bind('click.printPreview', function(e)
			{
				e.preventDefault();
			});
			// animation
			var starting_position = $(window).height() + $(window).scrollTop();
			var css = {
				top : starting_position,
				height : '100%',
				overflowY : 'auto',
				zIndex : 10000,
				display : 'block'
			}

			print_modal.css(css).animate({
				top : $(window).scrollTop()
			}, 400, 'linear', function()
			{
			});
			// Load mask
			$.printPreview.loadMask();
			// remove body over flow
			$('body').css({
				overflow : 'hidden'
			});
			// add listener click
			$('a', print_controls).bind('click', function(e)
			{
				e.preventDefault();
				if ($(this).hasClass('print'))
				{
					window.frames["print-modal-content"].focus();
					window.frames["print-modal-content"].print();
				} else
				{
					$.printPreview.destroyPrintPreview();
				}
			});

		},
		destroyPrintPreview : function()
		{
			print_controls.fadeOut(100);
			print_modal.animate({
				top : $(window).scrollTop() - $(window).height(),
				opacity : 1
			}, 400, 'linear', function()
			{
				print_modal.remove();
				$('body').css({
					overflow : 'visible',
				});
			});
			mask.fadeOut('slow', function()
			{
				mask.remove();
			});

			$(document).unbind("keydown.printPreview.mask");
			mask.unbind("click.printPreview.mask");
			$(window).unbind("resize.printPreview.mask");
		},
		loadMask : function()
		{
			size = $.printPreview.sizeUpMask();
			mask = $('<div id="print-modal-mask" />').appendTo($('body'));
			mask.css({
				position : 'absolute',
				top : 0,
				left : 0,
				width : size[0],
				height : size[1],
				display : 'none',
				opacity : 0,
				zIndex : 9999,
				backgroundColor : '#000'
			});

			mask.css({
				display : 'block'
			}).fadeTo('400', 0.75);

			$(window).bind("resize..printPreview.mask", function()
			{
				$.printPreview.updateMaskSize();
			});

			mask.bind("click.printPreview.mask", function(e)
			{
				$.printPreview.destroyPrintPreview();
			});
		},
		sizeUpMask : function()
		{
			if ($.browser.msie)
			{
				// if there are no scrollbars then use window.height
				var d = $(document).height(), w = $(window).height();
				return [ window.innerWidth || // ie7+
				document.documentElement.clientWidth || // ie6
				document.body.clientWidth, // ie6 quirks mode
				d - w < 20 ? w : d ];
			} else
			{
				return [ $(document).width(), $(document).height() ];
			}
		},

		updateMaskSize : function()
		{
			var size = $.printPreview.sizeUpMask();
			mask.css({
				width : size[0],
				height : size[1]
			});
		},
	}
})(jQuery);