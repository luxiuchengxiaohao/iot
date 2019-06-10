$('.weui-tabbar__item').tap(function(e){
    var self = $(this);
    self.siblings().removeClass('weui-bar__item_on');
    self.addClass('weui-bar__item_on');
});


