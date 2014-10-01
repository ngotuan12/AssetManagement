/**
 * @author: TuanNA
 * @since: 29/09/2014
 * @version: 1.0
 * @copyright Copyright (c) 2014, Ngo Anh Tuan
 * @require bootstrap jquery
 * @function
 *  init
 *  success
 *  error
 *  confirm
 */
(function($)
{
	$.message = {
		/**
		 * @author TuanNA
		 * @param
		 *   message: <strong> require </strong>
		 *   options: optional
		 */
		error : function(message,options)
		{
			if (typeof options !== 'object')
				options = {};
			options.class_name = 'alert alert-danger';
			if(typeof options.title !== 'string')
				options.title = '<h4> FMS Management System </h4>';
			if(typeof options.css !== 'object')
				options.css = {
						'position' : 'absolute',
						'left': '35%',
						'top': '30%',
						'z-index': '10000',
						'width' :'30%',
				};
			options.type = 'error';
			return $.message.init(message,options);
		},
		/**
		 * @author TuanNA
		 * @param
		 *   message: <strong> require </strong>
		 *   options: optional
		 */
		warning : function(message,options)
		{
			if (typeof options !== 'object')
				options = {};
			options.class_name = 'alert alert-warning';
			if(typeof options.title !== 'string')
				options.title = '<h4> FMS Management System </h4>';
			if(typeof options.css !== 'object')
				options.css = {
						'position' : 'absolute',
						'left': '35%',
						'top': '30%',
						'z-index': '10000',
						'width' :'30%',
				};
			options.type = 'warning';
			return $.message.init(message,options);
		},
		/**
		 * @author TuanNA
		 * @param
		 *   message: <strong> require </strong>
		 *   options: optional
		 */
		success : function(message,options)
		{
			if (typeof options !== 'object')
				options = {};
			options.class_name = 'alert alert-success';
			if(typeof options.title !== 'string')
				options.title = '<h4> FMS Management System </h4>';
			if(typeof options.css !== 'object')
				options.css = {
						'position' : 'absolute',
						'left': '35%',
						'top': '30%',
						'z-index': '10000',
						'width' :'30%',
				};
			options.type = 'success';
			return $.message.init(message,options);
		},
		/**
		 * @author TuanNA
		 * @param
		 *   message: <strong> require </strong>
		 *   position: optional
		 *     default: center
		 *     value: top,bottom,center
		 *   options: optional
		 */
		notification : function(message,position,options)
		{
			if (typeof options !== 'object')
				options = {};
			if(typeof options.class_name === 'undefined')
				options.class_name = 'alert alert-success';
			if(typeof options.mask === 'undefined')
				options.mask = false;
			if(typeof options.timeout === 'undefined')
				options.timeout = 5000;
			//position
			if(typeof position === 'undefined')
				position = 'center';
			if(position === 'top')
				options.css = {
						'position' : 'absolute',
						'z-index': '10000',
						'width' :'100%',
						'top':0,
						'text-align': 'center',
				};
			options.type = 'notification';
			return $.message.init(message,options);
		},
		/**
		 * @author TuanNA
		 * @param
		 *   message: <strong> require </strong>
		 *   position: optional
		 *     default: center
		 *     value: top,bottom,center
		 *   options: optional
		 */
		notice_error : function(message,position,options)
		{
			if (typeof options !== 'object')
				options = {};
			if(typeof options.class_name === 'undefined')
				options.class_name = 'alert alert-danger';
			if(typeof options.mask === 'undefined')
				options.mask = false;
			if(typeof options.timeout === 'undefined')
				options.timeout = 5000;
			//position
			if(typeof position === 'undefined')
				position = 'center';
			if(position === 'top')
				options.css = {
						'position' : 'absolute',
						'z-index': '10000',
						'width' :'100%',
						'top':0,
						'text-align': 'center',
				};
			options.type = 'notification';
			return $.message.init(message,options);
		},
		/**
		 * @author TuanNA
		 * @param
		 *   message: <strong> require </strong>
		 */
		confirm: function(message,options)
		{
			if (typeof options !== 'object')
				options = {};
			if(typeof options.title !== 'string')
				options.title = '<h4> FMS Management System </h4>';
			if(typeof options.css !== 'object')
				options.css = {
						'position' : 'absolute',
						'left': '35%',
						'top': '30%',
						'z-index': '10000',
						'width' :'30%',
				};
			options.type = 'confirm';
			
			return $.message.init(message,options);
		},
		/**
		 * @author TuanNA
		 * @param
		 *   message: <strong> require </strong>
		 *   options: optional
		 * @options
		 *  type: String. Value 'error','confirm','success'
		 *  calss_name: String
		 *  css: Object
		 *  timeout: number
		 *  mask: boolean
		 *  opacity: number 
		 *   >=0 <=1 available when mask = True
		 *   default 0.5
		 *  footer: text, html
		 */
		init: function(message,options)
		{
			var message_box = $('<div id="message-box"> </div>');
			
			//button dismiss
			var close_button = $('<button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button>');
			close_button.appendTo(message_box);
			//options
			if (typeof options !== 'object')
			{
				options = {};
			}
			//title
			if (typeof options.title === 'string')
			{
				var title = $('<div style="border-bottom: 1px solid;margin-bottom: 10px;">'+options.title+'</div>');
				message_box.append(title);
			}
			//message
			message_block = $('<div></div>')
			message_block.append(message);
			message_box.append(message_block);
			//class name
			var class_name = "alert alert-info fade in nomargin";
			if(typeof options.class_name === 'string')
			{
				class_name = options.class_name;
			}
			message_box.attr('class',class_name);
			// check css
			var css = {
				'position' : 'absolute',
				'left': '40%',
				'top': '40%',
				'z-index': '10000',
				'width' :'20%',
			};
			if(typeof options.css !=='undefined')
				css = options.css;
			message_box.css(css);
			//mask
			var is_mask = true;
			if(typeof options.mask === 'boolean')
			{
				is_mask = options.mask
			}
			
			if(is_mask)
			{
				//opacity
				var opacity = 0.5;
				if(typeof options.opacity ==='number' && options.opacity >=0 && options.opacity <=1 )
					opacity = options.opacity;
				//create mask
				mask = $('<div id="background-mask" />');
				mask.css({
					position : 'fixed',
					top : 0,
					left : 0,
					width : '100%',
					height : '100%',
					display : 'block',
					opacity : opacity,
					zIndex : 9999,
					backgroundColor : '#000'
				});
				
				mask.appendTo($('body'));
			}
			//type
			var control;
			var btnOK;
			var btnCancel;
			if(typeof options.type ==='string')
			{
				if(options.type === "confirm")
				{
					control = $('<div style="text-align:center;margin-top: 10px;"></div>');
					btnOK =  $('<button style="width:30%;margin-right:10px;" class="btn btn-info" type="button">Thực hiện</button>');
					btnCancel = $('<button style="width:30%;" class="btn btn-white" type="button">Thoát</button>');
				}
				else if(options.type === "error")
				{
					control = $('<div style="text-align:center;margin-top: 10px;"></div>');
					btnCancel =  $('<button style="width:30%;" class="btn btn-danger" type="button">Chấp nhận</button>');
				}
				else if(options.type === "success")
				{
					control = $('<div style="text-align:center;margin-top: 10px;"></div>');
					btnCancel =  $('<button style="width:30%;" class="btn btn-success" type="button">Chấp nhận</button>');
				}
				else if(options.type === "warning")
				{
					control = $('<div style="text-align:center;margin-top: 10px;"></div>');
					btnCancel =  $('<button style="width:30%;" class="btn btn-warning" type="button">Chấp nhận</button>');
				}
			}
			if(typeof btnOK !=='undefined')
			{
				btnOK.appendTo(control);
				//
				btnOK.on('click', function () 
				{
					$('#message-box').trigger("message.confirm");
				});
			}
			if(typeof btnCancel !=='undefined')
			{
				btnCancel.appendTo(control);
				//
				btnCancel.on('click', function () 
				{
					$('#message-box').alert('close')
				});
			}
			if(typeof control !=='undefined')
				control.appendTo(message_box);
			//footer
			if(typeof options.footer ==='string')
			{
				var footer_block = $('<div></div>')
				footer_block.append(footer);
				message_box.append(footer_block);
			}
			
			//add to body
			message_box.appendTo($('body'));
			//time out
			if(typeof options.timeout ==='number')
			{
				message_box.fadeOut(options.timeout,function(){
					$('#message-box').alert('close');
				});
			}
			// listener 
			$('#message-box').on('closed.bs.alert', function () 
			{
				if(typeof mask !== 'undefined')
					mask.remove();
				$('#message-box').trigger("message.close");
			});
			
			//return
			return message_box;
		},
		destroy: function()
		{
			$('#message-box').alert('close');
		},
	};

})(jQuery);
