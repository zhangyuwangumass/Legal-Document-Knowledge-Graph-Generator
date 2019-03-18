$(function(){
//当键盘键被松开时发送Ajax获取数据
		$('#text').keyup(function(){
			var keywords = $(this).val();
			if (keywords=='') { $('#word').hide(); return };


            $.ajax({
                url: 'http://127.0.0.1:5000/search?keyword=' + keywords,
                dataType: 'json',
                //contentType: 'application/text',
                //jsonp: 'cb', //回调函数的参数名(键值)key
                // jsonpCallback: 'fun', //回调函数名(值) value
                beforeSend:function(){
                    $('#word').append('<div>正在加载。。。</div>');
                },
                success:function(data){
                    alert('success worked')
                    $('#word').empty().show();
                    if(data==''){
                        $('#word').append('<div class="error">Not find  "' + keywords + '"</div>');
                    }
                    $('#word').append('<div class="click_work">'+ this +'</div>');
                    /**
                     if (data.s=='')
                     {
                         $('#word').append('<div class="error">Not find  "' + keywords + '"</div>');
                     }
                     $.each(data.s, function(){
						$('#word').append('<div class="click_work">'+ this +'</div>');
					})
                     **/
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {

                    //alert('status is ' + XMLHttpRequest.status);
                    //alert('readyState is ' + XMLHttpRequest.readyState);
                    //alert('textStatus is ' + textStatus);
                    alert('responseText is ' + JSON.stringify(XMLHttpRequest));

                    $('#word').empty().show();
                    $('#word').append('<div class="click_work">Fail "' + keywords + '"</div>');
                }
            })
		})
//点击搜索数据复制给搜索框
		$(document).on('click','.click_work',function(){
			var word = $(this).text();
			$('#text').val(word);
			$('#word').hide();
			// $('#texe').trigger('click');触发搜索事件
		})

	})